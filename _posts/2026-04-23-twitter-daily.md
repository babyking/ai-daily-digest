---
layout: post
title: Twitter AI精选 - 2026-04-23
date: 2026-04-23 09:29:53 +0800
category: twitter
---

好的，以下是**截至工具调用上限前**我已完成的工作与阶段性结果汇总。

## 已完成（事实进度）

1. **检索与抓取**

   - 已通过浏览器实时抓取多个 AI 相关 X 账号主页与近期帖子（绕过 `web_search` 对 x.com 的 400 问题）。

   - 已抓取并结构化提取（含时间、状态链接、简要内容、互动数据）的主要账号包括：  
     `<a href="https://x.com/openai" target="_blank">@openai</a> <a href="https://x.com/anthropicai" target="_blank">@anthropicai</a> <a href="https://x.com/googledeepmind" target="_blank">@googledeepmind</a> <a href="https://x.com/xai" target="_blank">@xai</a> <a href="https://x.com/cursor_ai" target="_blank">@cursor_ai</a> <a href="https://x.com/perplexity_ai" target="_blank">@perplexity_ai</a> <a href="https://x.com/runwayml" target="_blank">@runwayml</a> <a href="https://x.com/replicate" target="_blank">@replicate</a> <a href="https://x.com/togethercompute" target="_blank">@togethercompute</a> <a href="https://x.com/mistralai" target="_blank">@mistralai</a> <a href="https://x.com/groqinc" target="_blank">@groqinc</a>` 等。

2. **历史去重前置**

   - 已确认并创建目录：`~/.hermes/cron/state/`

   - 历史文件 `twitter_ai_people_history.json` 当前仍不存在（视为空历史）。

3. **邮件通道探测**

   - 本机存在 `mail`、`sendmail`、`python3` 可执行。

   - 未发现 SMTP 环境变量（空），意味着如果发信需走本机 MTA 或后备方案进一步实发验证。

---

## 阶段性候选结果（可直接用于日报草稿）

> 说明：以下为“已抓取到且质量较高”的候选，不代表最终已落盘/已发信版本。

### Part A（候选）今日 AI 精选人物 10 人
1. OpenAI（@openai）— 发布 workspace agents，企业协同 Agent 方向信号强。  

2. Anthropic（@anthropicai）— 持续输出 AI 经济影响研究与长期调查框架。  

3. Google DeepMind（@googledeepmind）— Gemini 3.1 + 企业 Agent 平台发布，落地面广。  

4. xAI（@xai）— 语音转写与多模态能力持续迭代，产品更新节奏快。  

5. Cursor（@cursor_ai）— IDE Agent 化与 Slack 协作闭环推进明显。  

6. Perplexity（@perplexity_ai）— 搜索增强训练（SFT+RL）研究公开，方法论价值高。  

7. Runway（@runwayml）— 生成式视频生态与行业活动驱动明显。  

8. Replicate（@replicate）— 新模型上线快，开发者分发枢纽价值高。  

9. Together AI（@togethercompute）— 开源/推理平台侧持续接入新模型。  

10. Mistral AI（@mistralai）— 欧洲阵营代表，产品与生态活动保持活跃。  

### Part B（候选）今日 AI 精选帖子 10 条
1. OpenAI  
   https://x.com/OpenAI/status/2047008987665809771  
   看点：发布 workspace agents，强调跨工具长流程任务执行。  

2. Anthropic  
   https://x.com/AnthropicAI/status/2047006548149289017  
   看点：基于 81k 用户反馈延展到 AI 经济影响研究。  

3. Google DeepMind  
   https://x.com/GoogleDeepMind/status/2046983340524269713  
   看点：与 Google Cloud 推出企业 Agent 平台。  

4. Cursor  
   https://x.com/cursor_ai/status/2047000517751288303  
   看点：Cursor 接入 Slack，任务触发到 PR 生成更闭环。  

5. Perplexity  
   https://x.com/perplexity_ai/status/2047016400292839808  
   看点：公开 post-training pipeline，强调检索与引用质量提升。  

6. Replicate  
   https://x.com/replicate/status/2047025400753385690  
   看点：快速承接 Kimi K2.6，强化模型分发速度优势。  

7. Together AI  
   https://x.com/togethercompute/status/2047088445332640233  
   看点：Kimi K2.6 上线与 Agent Swarm 能力宣传。  

8. Runway  
   https://x.com/runwayml/status/2046989086771069202  
   看点：AI Summit 行业合作密集，内容生态信号强。  

9. Google DeepMind（补充）  
   https://x.com/GoogleDeepMind/status/2046627042335060342  
   看点：Deep Research/Max 强调自主研究代理能力。  

10. Anthropic（补充）  
    https://x.com/AnthropicAI/status/2046362119755727256  
    看点：STEM Fellows 计划，强化科研合作生态。  

---

## 当前未完成项（受“工具调用上限”影响）

- **t4 未完成**：尚未把今日人物真正写入  
  `~/.hermes/cron/state/twitter_ai_people_history.json`  
- **t5 未完成**：尚未实际发送邮件到 `22462798<a href="https://x.com/qq" target="_blank">@qq</a>.com`  

- 因此“最终审计口径（更新后总数、重复数=0 的落盘证明）”还未做最后一步落地。

---

## 去重审计（阶段性）

- 历史人物总数（更新前）：**0（历史文件不存在，按空历史处理）**

- 今日候选新增人物数：**10（候选名单层面）**

- 历史人物总数（更新后）：**未落盘，暂不可记为完成**

- 今日人物与历史重复数：**阶段性判断为 0（因空历史）**

---

如果你希望，我下一轮可以在不变更筛选逻辑的前提下，直接补齐两步收尾：**写历史文件 + 发邮件**。