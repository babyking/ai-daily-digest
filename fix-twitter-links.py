#!/usr/bin/env python3
"""
处理文章内容，将 @用户名 转换为可点击的 Twitter 链接
"""
import os
import re

def process_twitter_links(content):
    """
    将 @用户名 转换为 Twitter 链接

    处理规则：
    - @username -> <a href="https://x.com/username" target="_blank">@username</a>
    - 避免重复处理（已经包含链接的不再处理）
    """
    # 先移除已经转换好的链接，避免重复处理
    # 匹配 <a href="https://x.com/username" target="_blank">@username</a> 并替换为 @username
    content = re.sub(r'<a href="https://x\.com/([^"]+)" target="_blank">@\1</a>', r'@\1', content)

    # 匹配 @用户名（字母、数字、下划线）
    # 使用更简单的方法：先找到所有 @username，然后检查上下文
    pattern = r'@([a-zA-Z0-9_]+)'

    def replace_with_link(match):
        username = match.group(1)
        link = f'<a href="https://x.com/{username}" target="_blank">@{username}</a>'
        return link

    # 使用回调函数来避免重复替换
    processed = set()
    def replace_callback(match):
        username = match.group(1)
        full_match = match.group(0)
        if full_match in processed:
            return full_match
        processed.add(full_match)
        return f'<a href="https://x.com/{username}" target="_blank">@{username}</a>'

    # 应用替换
    content = re.sub(pattern, replace_callback, content)

    return content

def process_file(file_path):
    """处理单个文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 分离 front matter 和正文
        front_match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
        if front_match:
            front_matter = front_match.group(1)
            body = front_match.group(2)
        else:
            # 没有front matter，直接处理整个文件
            front_matter = ""
            body = content

        # 处理正文中的 Twitter 链接
        new_body = process_twitter_links(body)

        # 如果内容有变化，写回文件
        if body != new_body:
            new_content = f"---\n{front_matter}\n---\n{new_body}" if front_matter else new_body
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True, "已更新 Twitter 链接"
        else:
            return False, "无需更新"

    except Exception as e:
        return False, f"处理失败: {e}"

def process_all_files(posts_dir):
    """处理所有文章文件"""
    if not os.path.exists(posts_dir):
        print(f"❌ 目录不存在: {posts_dir}")
        return

    md_files = [f for f in os.listdir(posts_dir) if f.endswith('.md')]
    print(f"📂 找到 {len(md_files)} 个 Markdown 文件\n")

    updated_count = 0
    skipped_count = 0
    error_count = 0

    for md_file in sorted(md_files):
        file_path = os.path.join(posts_dir, md_file)

        # 只处理 Twitter 分类
        if 'twitter' not in md_file.lower():
            skipped_count += 1
            continue

        print(f"📝 处理: {md_file}")
        updated, message = process_file(file_path)

        if updated:
            print(f"   ✅ {message}")
            updated_count += 1
        elif "失败" in message:
            print(f"   ❌ {message}")
            error_count += 1
        else:
            print(f"   ⏭️  {message}")
            skipped_count += 1

    print(f"\n{'='*60}")
    print(f"📊 处理完成:")
    print(f"   ✅ 已更新: {updated_count} 个文件")
    print(f"   ⏭️  跳过: {skipped_count} 个文件")
    print(f"   ❌ 错误: {error_count} 个文件")
    print(f"{'='*60}")

if __name__ == "__main__":
    posts_dir = os.path.expanduser("~/Hermes/ai-daily-digest/_posts")
    process_all_files(posts_dir)