# AI Daily Digest - 使用说明

## 🌐 网站信息
- **网址**: https://babyking.github.io/ai-daily-digest/
- **仓库**: https://github.com/babyking/ai-daily-digest
- **本地路径**: `~/Hermes/ai-daily-digest`

## 📋 功能特性

### 1. 内容分类
- **Reddit精选**: 从 Reddit AI 相关社区收集热门讨论
- **Twitter精选**: 从 Twitter/X 收集 AI 领域有价值推文
- **音乐技术**: 收集音乐制作和音频技术相关内容

### 2. 筛选功能
- 按分类筛选（全部/Reddit/Twitter/音乐技术）
- 按时间筛选（全部/最近7天/最近30天）
- 统计信息展示（总文章数、各分类数量）

### 3. 自动发布
- 每日自动收集内容
- 自动推送到 GitHub Pages
- 网站自动更新（通常1-3分钟）

## 🚀 工作流程

### 1. 定时任务（Cronjob）

**Reddit 精选** (每日 08:50)
- 任务ID: `995add06a7fe`
- 收集 r/MachineLearning, r/ArtificialIntelligence 等社区内容
- 输出到: `~/.hermes/cron/output/995add06a7fe/`

**Twitter 精选** (每日 08:50)
- 任务ID: `2a421cfee1ac`
- 收集 AI 领域知名人士推文
- 输出到: `~/.hermes/cron/output/2a421cfee1ac/`

**音乐技术** (每日 09:00)
- 任务ID: `64255f69f9b1`
- 收集音乐制作技术相关内容
- 输出到: `~/.hermes/cron/output/64255f69f9b1/`

### 2. 自动推送（监控脚本）

监控脚本会自动检测新内容并推送到 GitHub：

```bash
# 启动监控脚本（后台运行）
nohup python3 ~/Hermes/ai-daily-digest/watch-and-push.py &

# 或者单次检查
python3 ~/Hermes/ai-daily-digest/watch-and-push.py
```

监控脚本特性：
- 每5分钟检查一次新内容
- 自动跳过空内容和已推送文件
- 自动调用 `push-to-github.py` 推送到 GitHub
- 状态保存在 `.watch-state.json`

### 3. GitHub 自动构建

- 内容推送到 GitHub 后
- GitHub Pages 自动构建网站
- 通常需要 1-3 分钟完成
- 网站自动更新

## 🔧 维护命令

### 查看监控脚本状态
```bash
ps aux | grep watch-and-push.py
```

### 停止监控脚本
```bash
pkill -f watch-and-push.py
```

### 手动推送特定文件
```bash
cd ~/Hermes/ai-daily-digest
python3 push-to-github.py reddit ~/.hermes/cron/output/995add06a7fe/2026-05-09_08-50-00.md
```

### 导入历史数据
```bash
cd ~/Hermes/ai-daily-digest
python3 import-cron-output.py
```

### 查看 Git 状态
```bash
cd ~/Hermes/ai-daily-digest
git status
git log --oneline -10
```

## 📁 目录结构

```
~/Hermes/ai-daily-digest/
├── _config.yml              # Jekyll 配置文件
├── index.html               # 首页（含筛选功能）
├── _layouts/
│   └── default.html         # 默认布局
├── _posts/                  # 文章目录
│   ├── 2026-05-09-reddit-daily.md
│   ├── 2026-05-09-twitter-daily.md
│   └── ...
├── assets/                  # 静态资源
├── push-to-github.py        # 推送脚本
├── watch-and-push.py        # 监控脚本
├── import-cron-output.py    # 导入脚本
├── push-to-github.sh        # Shell 推送脚本（备用）
└── .watch-state.json        # 监控状态文件
```

## ⚙️ 配置说明

### 筛选功能
网站使用 JavaScript 实现客户端筛选：
- **分类筛选**: 根据 `data-category` 属性筛选
- **时间筛选**: 根据 `data-date` 属性和当前日期计算
- **响应式设计**: 支持移动端和桌面端

### Jekyll 配置
- **Markdown**: kramdown
- **语法高亮**: rouge
- **分页**: 每页10篇文章
- **URL格式**: `/:categories/:year/:month/:day/:title/`

## 🎯 规则说明

### SILENT 模式
如果当天没有找到有价值的内容（少于3条），任务会输出 `[SILENT]`，不会推送任何内容，也不会发送通知。

### 质量标准
- Reddit: 只选择有实质讨论、能引发思考的帖子
- Twitter: 只选择有价值信息、技术见解的推文
- 音乐技术: 只选择实用教程、行业动态

### 时间范围
- 只收集最近24小时内的新内容
- 推送时会自动包含文件创建时间
- 网站按时间倒序排列

## 🔍 故障排查

### 网站未更新
1. 检查监控脚本是否运行: `ps aux | grep watch-and-push.py`
2. 检查 GitHub Actions 构建状态
3. 等待 3-5 分钟让 GitHub Pages 完成构建

### 内容未推送
1. 检查 cron 输出目录是否有新文件
2. 查看监控日志: `tail -f nohup.out`
3. 手动测试推送脚本

### 推送失败
1. 检查 SSH 密钥配置
2. 测试 GitHub 连接: `ssh -T git@github.com`
3. 查看错误日志

## 📊 数据统计

当前数据（截至 2026-05-09）:
- 总文章数: 41
- Reddit精选: 18 篇
- Twitter精选: 21 篇
- 音乐技术: 2 篇
- 时间范围: 2026-04-19 至 2026-05-09

## 🎉 使用技巧

1. **快速浏览**: 使用"最近7天"筛选查看最新内容
2. **特定兴趣**: 使用分类筛选只关注某个类别
3. **移动端**: 支持手机访问，响应式布局
4. **直接链接**: 每篇文章都有独立URL，可分享

## 📞 支持

如有问题或建议，请：
1. 查看 GitHub Issues
2. 检查本项目的 README.md
3. 查看监控脚本日志文件

---

最后更新: 2026-05-09