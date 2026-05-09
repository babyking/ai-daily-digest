#!/usr/bin/env python3
"""
将cronjob输出转换为Jekyll文章格式
"""
import os
import re
from datetime import datetime

# 任务ID到分类的映射
TASK_TO_CATEGORY = {
    "995add06a7fe": "reddit",
    "2a421cfee1ac": "twitter",
    "64255f69f9b1": "music"
}

# 分类到名称的映射
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
        # 提取Response之后的内容
        actual_content = content[response_match.end():].strip()
    else:
        # 如果没有Response标记，尝试从第一个一级标题开始提取
        title_match = re.search(r'^# ', content, re.MULTILINE)
        if title_match:
            actual_content = content[title_match.start():].strip()
        else:
            # 如果都没有，返回整个文件内容（跳过prompt部分）
            lines = content.split('\n')
            # 跳过开头的prompt相关内容，找到第一个有意义的内容
            start_idx = 0
            for i, line in enumerate(lines):
                if line.startswith('# ') or line.startswith('## ') or line.startswith('---'):
                    start_idx = i
                    break
            actual_content = '\n'.join(lines[start_idx:]).strip()

    return actual_content

def extract_title(content):
    """从内容中提取标题"""
    # 查找第一个一级标题
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if title_match:
        return title_match.group(1).strip()
    return "无标题"

def parse_filename(filename):
    """解析文件名，提取日期和时间"""
    # 格式: YYYY-MM-DD_HH-MM-SS.md
    match = re.match(r'(\d{4}-\d{2}-\d{2})_(\d{2}-\d{2}-\d{2})\.md', filename)
    if match:
        date_str = match.group(1)
        time_str = match.group(2).replace('-', ':')
        return f"{date_str} {time_str}"
    return None

def convert_to_jekyll_post(input_file, task_id, output_dir):
    """将cronjob输出转换为Jekyll文章"""
    # 提取日期和分类
    filename = os.path.basename(input_file)
    datetime_str = parse_filename(filename)

    if not datetime_str:
        print(f"⚠️  跳过 {filename}: 无法解析日期")
        return False

    category = TASK_TO_CATEGORY.get(task_id, "unknown")
    category_name = CATEGORY_TO_NAME.get(category, "未知分类")

    # 读取并提取内容
    actual_content = extract_content_from_markdown(input_file)

    if not actual_content or len(actual_content) < 50:
        print(f"⚠️  跳过 {filename}: 内容为空或过短")
        return False

    # 提取标题
    title = extract_title(actual_content)
    full_title = f"{category_name} - {datetime_str.split()[0]}"

    # 生成Jekyll front matter
    front_matter = f"""---
layout: post
title: {full_title}
date: {datetime_str} +0800
category: {category}
---

"""

    # 写入文件
    output_filename = f"{datetime_str.split()[0]}-{category}-daily.md"
    output_path = os.path.join(output_dir, output_filename)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(front_matter)
        f.write(actual_content)

    print(f"✅ 已创建: {output_filename}")
    return True

def main():
    """主函数"""
    cron_output_dir = os.path.expanduser("~/.hermes/cron/output")
    posts_dir = os.path.expanduser("~/Hermes/ai-daily-digest/_posts")

    # 确保输出目录存在
    os.makedirs(posts_dir, exist_ok=True)

    # 遍历所有任务目录
    task_dirs = {
        "995add06a7fe": "Reddit",
        "2a421cfee1ac": "Twitter",
        "64255f69f9b1": "Music"
    }

    total_processed = 0
    total_skipped = 0

    for task_id, task_name in task_dirs.items():
        task_path = os.path.join(cron_output_dir, task_id)

        if not os.path.exists(task_path):
            print(f"⚠️  任务目录不存在: {task_path}")
            continue

        # 遍历该任务的所有输出文件
        files = sorted([f for f in os.listdir(task_path) if f.endswith('.md')])

        for filename in files:
            input_file = os.path.join(task_path, filename)

            # 跳过今天的测试文件
            if "2026-05-09" in filename and "reddit-daily.md" in filename:
                continue

            if convert_to_jekyll_post(input_file, task_id, posts_dir):
                total_processed += 1
            else:
                total_skipped += 1

    print(f"\n📊 处理完成:")
    print(f"   成功: {total_processed} 篇")
    print(f"   跳过: {total_skipped} 篇")

if __name__ == "__main__":
    main()