#!/usr/bin/env python3
"""
优化文章的段落结构，让长内容更易读

处理规则：
1. 在每个列表项之间添加空行（提高可读性）
2. 在主要部分之间添加空行
3. 确保段落之间有适当的空行
4. 保持原有的格式和结构
"""
import os
import re

def optimize_content(content):
    """
    优化内容的段落结构
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
            front_matter = ""
            body = content

        # 处理正文
        new_body = optimize_content(body)

        # 如果内容有变化，写回文件
        if body != new_body:
            new_content = f"---\n{front_matter}\n---\n{new_body}" if front_matter else new_body
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True, "已优化段落结构"
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
    print(f"   ✅ 已优化: {updated_count} 个文件")
    print(f"   ⏭️  跳过: {skipped_count} 个文件")
    print(f"   ❌ 错误: {error_count} 个文件")
    print(f"{'='*60}")

if __name__ == "__main__":
    posts_dir = os.path.expanduser("~/Hermes/ai-daily-digest/_posts")
    process_all_files(posts_dir)