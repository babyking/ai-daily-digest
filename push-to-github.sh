#!/bin/bash
# 将内容提交到GitHub的脚本

# 配置
REPO_DIR="$HOME/Hermes/ai-daily-digest"
CATEGORY="$1"
TITLE="$2"
CONTENT_FILE="$3"
DATE=$(date +%Y-%m-%d)

if [ -z "$CATEGORY" ] || [ -z "$TITLE" ] || [ -z "$CONTENT_FILE" ]; then
    echo "使用方法: $0 <category> <title> <content_file>"
    echo "示例: $0 reddit 'Reddit AI精选 2026-05-09' /path/to/content.md"
    exit 1
fi

if [ ! -f "$CONTENT_FILE" ]; then
    echo "错误: 内容文件不存在: $CONTENT_FILE"
    exit 1
fi

# 创建markdown文件（Jekyll格式）
POST_FILE="$REPO_DIR/_posts/${DATE}-${CATEGORY}-daily.md"

# 添加Jekyll front matter
cat > "$POST_FILE" << EOF
---
layout: post
title: $TITLE
date: $(date +"%Y-%m-%d %H:%M:%S +0800")
category: $CATEGORY
---

EOF

# 追加内容
cat "$CONTENT_FILE" >> "$POST_FILE"

# 提交到Git
cd "$REPO_DIR"
git add _posts/
git commit -m "[$CATEGORY] $TITLE - $DATE"
git push origin main

echo "✅ 已提交到GitHub: $POST_FILE"