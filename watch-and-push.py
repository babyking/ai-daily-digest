#!/usr/bin/env python3
"""
监控 cron 输出目录，自动推送新内容到 GitHub

运行方式：
1. 后台运行：nohup python3 ~/Hermes/ai-daily-digest/watch-and-push.py &
2. 或使用 systemd/cron 定期运行
"""
import os
import time
import subprocess
import json
from datetime import datetime, timedelta

# 配置
REPO_DIR = os.path.expanduser("~/Hermes/ai-daily-digest")
STATE_FILE = os.path.join(REPO_DIR, ".watch-state.json")
CHECK_INTERVAL = 300  # 检查间隔（秒），默认5分钟

# 任务ID到分类的映射
TASK_TO_CATEGORY = {
    "995add06a7fe": "reddit",
    "2a421cfee1ac": "twitter",
    "64255f69f9b1": "music"
}

def load_state():
    """加载状态文件"""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {"last_check": None, "pushed_files": {}}

def save_state(state):
    """保存状态文件"""
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def get_latest_file(task_id):
    """获取指定任务ID的最新输出文件"""
    output_dir = f"~/.hermes/cron/output/{task_id}"
    output_dir = os.path.expanduser(output_dir)

    if not os.path.exists(output_dir):
        return None

    # 获取最新的文件
    files = [f for f in os.listdir(output_dir) if f.endswith('.md')]
    if not files:
        return None

    # 按修改时间排序
    files.sort(key=lambda f: os.path.getmtime(os.path.join(output_dir, f)), reverse=True)

    return os.path.join(output_dir, files[0])

def is_content_empty(file_path):
    """检查文件内容是否为空（实际内容部分）"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 查找 "## Response" 之后的内容
        import re
        response_match = re.search(r'## Response\s*\n', content)

        if response_match:
            actual_content = content[response_match.end():].strip()
        else:
            lines = content.split('\n')
            start_idx = 0
            for i, line in enumerate(lines):
                if line.startswith('# ') or line.startswith('## '):
                    start_idx = i
                    break
            actual_content = '\n'.join(lines[start_idx:]).strip()

        # 检查是否为 SILENT 或过短
        if not actual_content or len(actual_content) < 50:
            return True

        if actual_content.startswith('[SILENT]'):
            return True

        return False

    except Exception as e:
        print(f"⚠️  检查文件内容时出错: {e}")
        return True

def push_to_github(category, file_path):
    """调用推送脚本"""
    push_script = os.path.join(REPO_DIR, "push-to-github.py")

    try:
        result = subprocess.run(
            ['python3', push_script, category, file_path],
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode == 0:
            print(f"✅ 推送成功: {category} - {os.path.basename(file_path)}")
            return True
        else:
            print(f"❌ 推送失败: {category} - {os.path.basename(file_path)}")
            print(f"   错误: {result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        print(f"⏱️  推送超时: {category}")
        return False
    except Exception as e:
        print(f"❌ 推送异常: {e}")
        return False

def check_and_push():
    """检查并推送新内容"""
    state = load_state()
    current_time = datetime.now()
    pushed_count = 0

    print(f"\n{'='*60}")
    print(f"🕐 检查时间: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    for task_id, category in TASK_TO_CATEGORY.items():
        latest_file = get_latest_file(task_id)

        if not latest_file:
            print(f"⚠️  {category:10} - 未找到输出文件")
            continue

        file_mtime = datetime.fromtimestamp(os.path.getmtime(latest_file))
        file_name = os.path.basename(latest_file)

        # 检查是否是上次检查之后的新文件
        if state["last_check"] and file_mtime < state["last_check"]:
            print(f"⏭️  {category:10} - 已处理 ({file_name})")
            continue

        # 检查是否已经推送过
        if file_name in state.get("pushed_files", {}):
            print(f"⏭️  {category:10} - 已推送 ({file_name})")
            continue

        # 检查内容是否为空
        if is_content_empty(latest_file):
            print(f"⏭️  {category:10} - 内容为空 ({file_name})")
            # 标记为已处理，避免重复检查
            if "pushed_files" not in state:
                state["pushed_files"] = {}
            state["pushed_files"][file_name] = {
                "time": current_time.isoformat(),
                "skipped": True
            }
            continue

        # 推送到 GitHub
        print(f"📤 {category:10} - 开始推送 ({file_name})")
        success = push_to_github(category, latest_file)

        if success:
            if "pushed_files" not in state:
                state["pushed_files"] = {}
            state["pushed_files"][file_name] = {
                "time": current_time.isoformat(),
                "category": category
            }
            pushed_count += 1
        else:
            print(f"❌ {category:10} - 推送失败，下次重试")

    # 更新最后检查时间
    state["last_check"] = current_time.isoformat()

    # 清理旧的推送记录（保留最近7天）
    if "pushed_files" in state:
        cutoff = (current_time - timedelta(days=7)).isoformat()
        state["pushed_files"] = {
            k: v for k, v in state["pushed_files"].items()
            if v.get("time", "") > cutoff
        }

    save_state(state)

    print(f"\n✅ 检查完成，共推送 {pushed_count} 个文件")
    print(f"{'='*60}\n")

    return pushed_count > 0

def main():
    """主函数"""
    print("🚀 GitHub 自动推送监控脚本启动")
    print(f"📂 仓库目录: {REPO_DIR}")
    print(f"⏱️  检查间隔: {CHECK_INTERVAL} 秒")
    print(f"📋 监控任务: {', '.join(TASK_TO_CATEGORY.values())}")
    print("\n按 Ctrl+C 停止脚本\n")

    # 首次检查
    check_and_push()

    # 持续监控
    try:
        while True:
            time.sleep(CHECK_INTERVAL)
            check_and_push()
    except KeyboardInterrupt:
        print("\n\n👋 脚本已停止")

if __name__ == "__main__":
    main()