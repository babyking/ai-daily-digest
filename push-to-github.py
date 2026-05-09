#!/usr/bin/env python3
"""
Cronjob完成后自动推送内容到GitHub的脚本
用法: python3 push-to-github.py <category> <content_file>

示例:
  python3 push-to-github.py reddit ~/.hermes/cron/output/995add06a7fe/2026-05-09_08-50-00.md
  python3 push-to-github.py twitter ~/.hermes/cron/output/2a421cfee1ac/2026-05-09_08-50-00.md
  python3 push-to-github.py music ~/.hermes/cron/output/64255f69f9b1/2026-05-09_09-00-00.md
"""
import os
import re
import subprocess
import sys
from datetime import datetime

# 配置
REPO_DIR = os.path.expanduser("~/Hermes/ai-daily-digest")

# 任务ID到分类的映射
CATEGORY_TO_NAME = {
    "reddit": "Reddit AI精选",
    "twitter": "Twitter AI精选",
    "music": "音乐制作技术情报"
}

def extract_content_from_markdown(file_path):
    """从markdown文件中提取有效内容（跳过prompt部分）"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 查找 "## Response" 之后的内容
    response_match = re.search(r'## Response\s*\n', content)

    if response_match:
        actual_content = content[response_match.end():].strip()
    else:
        title_match = re.search(r'^# ', content, re.MULTILINE)
        if title_match:
            actual_content = content[title_match.start():].strip()
        else:
            lines = content.split('\n')
            start_idx = 0
            for i, line in enumerate(lines):
                if line.startswith('# ') or line.startswith('## '):
                    start_idx = i
                    break
            actual_content = '\n'.join(lines[start_idx:]).strip()

    return actual_content

def extract_title(content):
    """从内容中提取标题"""
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if title_match:
        return title_match.group(1).strip()
    return "无标题"

def parse_filename(filename):
    """解析文件名，提取日期和时间"""
    match = re.match(r'(\d{4}-\d{2}-\d{2})_(\d{2}-\d{2}-\d{2})\.md', filename)
    if match:
        date_str = match.group(1)
        time_str = match.group(2).replace('-', ':')
        return f"{date_str} {time_str}"
    return None

def optimize_paragraphs(content):
    """
    优化内容的段落结构，让长内容更易读

    处理规则：
    1. 在每个列表项之间添加空行（提高可读性）
    2. 在主要部分之间添加空行
    3. 确保段落之间有适当的空行
    """
    lines = content.split('\n')
    result = []

    for i, line in enumerate(lines):
        result.append(line)

        # 在列表项之间添加空行（提高可读性）
        list_match = re.match(r'^\s*[-*]\s+', line)
        numbered_match = re.match(r'^\s*\d+\.\s+', line)

        if list_match or numbered_match:
            # 检查下一个是否也是列表项
            if i + 1 < len(lines):
                next_list = re.match(r'^\s*[-*]\s+', lines[i + 1])
                next_numbered = re.match(r'^\s*\d+\.\s+', lines[i + 1])

                # 如果下一个也是列表项，在当前列表项后添加空行
                if next_list or next_numbered:
                    result.append('')

        # 在二级标题（##）后添加空行
        heading_match = re.match(r'^##\s+', line)
        if heading_match and i + 1 < len(lines) and lines[i + 1].strip():
            result.append('')

        # 在四级标题（####）后添加空行（通常是具体的小节）
        subheading_match = re.match(r'^####\s+', line)
        if subheading_match and i + 1 < len(lines) and lines[i + 1].strip():
            result.append('')

    # 移除过多的连续空行（最多保留1个）
    final_result = []
    prev_empty = False
    for line in result:
        if line.strip() == '':
            if not prev_empty:
                final_result.append(line)
                prev_empty = True
        else:
            final_result.append(line)
            prev_empty = False

    return '\n'.join(final_result)

def process_twitter_links(content):
    """
    将 Twitter 用户名转换为可点击链接
    """
    # 匹配 @username 格式（前面不是 / 或已经是链接的一部分）
    def replace_username(match):
        username = match.group(1)
        return f'<a href="https://x.com/{username}" target="_blank">@{username}</a>'

    # 排除已经是链接的情况（如 <a href="...">@username</a>）
    content = re.sub(r'(?<!href="https://x\.com/)(?<!>)@(\w+)', replace_username, content)
    return content

def push_to_github(category, content_file):
    """将内容推送到GitHub"""
    # 验证参数
    if not os.path.exists(content_file):
        print(f"❌ 错误: 文件不存在 - {content_file}")
        return False

    if category not in CATEGORY_TO_NAME:
        print(f"❌ 错误: 未知分类 - {category}")
        print(f"   可用分类: {', '.join(CATEGORY_TO_NAME.keys())}")
        return False

    # 解析日期
    filename = os.path.basename(content_file)
    datetime_str = parse_filename(filename)

    if not datetime_str:
        print(f"❌ 错误: 无法解析文件名中的日期 - {filename}")
        return False

    # 读取并提取内容
    actual_content = extract_content_from_markdown(content_file)

    if not actual_content or len(actual_content) < 50:
        print(f"⚠️  警告: 内容为空或过短，跳过推送")
        return False

    # 提取标题
    title = extract_title(actual_content)
    category_name = CATEGORY_TO_NAME[category]
    full_title = f"{category_name} - {datetime_str.split()[0]}"

    # 创建Jekyll文章
    posts_dir = os.path.join(REPO_DIR, "_posts")
    os.makedirs(posts_dir, exist_ok=True)

    output_filename = f"{datetime_str.split()[0]}-{category}-daily.md"
    output_path = os.path.join(posts_dir, output_filename)

    # 写入文件（包含Jekyll front matter）
    front_matter = f"""---
layout: post
title: {full_title}
date: {datetime_str} +0800
category: {category}
---

"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(front_matter)
        f.write(actual_content)

    # 优化段落结构
    with open(output_path, 'r', encoding='utf-8') as f:
        content = f.read()

    optimized_content = optimize_paragraphs(content)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(optimized_content)

    print(f"✅ 已优化段落结构")

    # 如果是 Twitter 内容，处理链接
    if category == "twitter":
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()

        processed_content = process_twitter_links(content)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(processed_content)

        print(f"✅ 已处理 Twitter 链接")

    print(f"✅ 已创建文章: {output_filename}")

    # Git操作
    os.chdir(REPO_DIR)

    try:
        # 添加文件
        subprocess.run(['git', 'add', f'_posts/{output_filename}'], check=True, capture_output=True)

        # 提交
        commit_message = f"[{category.upper()}] {full_title}"
        subprocess.run(['git', 'commit', '-m', commit_message], check=True, capture_output=True)

        # 推送
        subprocess.run(['git', 'push', 'origin', 'main'], check=True, capture_output=True)

        print(f"✅ 已推送到GitHub")
        print(f"   仓库: https://github.com/babyking/ai-daily-digest")
        print(f"   网站: https://babyking.github.io/ai-daily-digest/")

        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Git操作失败: {e}")
        if e.stderr:
            print(f"   错误信息: {e.stderr.decode('utf-8')}")
        return False
    except Exception as e:
        print(f"❌ 未知错误: {e}")
        return False

def main():
    """主函数"""
    if len(sys.argv) != 3:
        print("用法: python3 push-to-github.py <category> <content_file>")
        print("\n分类选项:")
        for cat, name in CATEGORY_TO_NAME.items():
            print(f"  {cat:10} - {name}")
        print("\n示例:")
        print("  python3 push-to-github.py reddit ~/.hermes/cron/output/995add06a7fe/2026-05-09_08-50-00.md")
        sys.exit(1)

    category = sys.argv[1]
    content_file = os.path.expanduser(sys.argv[2])

    push_to_github(category, content_file)

if __name__ == "__main__":
    main()
