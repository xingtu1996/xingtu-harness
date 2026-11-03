# 内容生产 Harness 接口契约（豆包侧蒸馏 · 2026-11-03）

> 关联：xingtu-harness issue #5（跨 Agent 资产蒸馏与接力）
> 本文件是豆包工作侧内容生产能力的**通用化接口契约**（脱敏版，不含私有路径/内部口径/个人数据）。完整版含真实资产映射，存私有 vault `交接中心/豆包内容蒸馏_2026-11-03/`。
> 目的：让 GPT / Codex / Muse 等 Agent 仅凭公开仓库即可调用「内容生产」能力，实现跨 Agent 无缝接力。

## 一、能力契约总表（7 项）

| capability | trigger（触发词示例） | inputs | outputs | gates | receipt |
|------|------|------|------|------|------|
| plan_article（选题） | 「今天发什么」「选题池有没有」 | 口径、时间窗、素材池状态 | 候选选题 + 依据 | 撞题检查、素材可溯源 | 选题卡/候选列表 |
| draft_article（写稿） | 「写这篇」「出初稿」「按 XX 改」 | 选题卡、素材引用、风格约束 | 正文 v1（Markdown） | 结构门禁 | 稿件路径 + 版本 |
| review_article（审稿） | 「发前核验」「能不能发」「dry-run」 | 正文、素材、发布目标 | 门禁报告（通过/拒绝+原因） | 去 AI 味、隐私、合规 | 门禁逐项结果 |
| illustrate（配图） | 「配图」「概念图」「图卡」 | 正文段落/概念锚点 | 图卡 + 概念说明 | 无水印、AI 图标识、尺寸 | 图卡清单 + 验收 |
| render_wechat（排版） | 「排版」「公众号版」 | 正文 md | 橙红主题 HTML | 主题规范、无本地路径 | 排版文件路径 |
| build_package（建包） | 「建包」「归档」「直转发布包」 | 正文、素材、合集信息 | 标准目录发布包 | 包结构规范、封面状态标记 | 包路径 + 索引登记 |
| verify_delivery（验收） | 「交付后核验」「回填凭证」 | 发布包/发布链接 | 验收回执（receipt） | 交接字段闭环、来源哈希 | receipt JSON |

## 二、交接字段（15 字段）

```
task_id / goal / trigger / source_refs / source_hash / capability /
agent / permissions / content_status / decision_log / artifacts /
quality_checks / next_action / acceptance / receipt
```

- source_hash：来源文件 sha256（可核验）
- content_status：已发 / 待发 / 冻结 / 证据不足 四态
- decision_log：关键决策 + 理由 + 时间戳（可追溯修改原因）
- receipt：机器可读 JSON（含 limits 字段诚实声明局限）

## 三、内容状态机

```
证据不足 ──门禁通过──> 待发 ──人工批准──> 已发
   ↑                        │              │
   └──── 冻结（已发不改）←─────────────────┘
```

## 四、跨 Agent 接力协议

1. 接手方先读交付包导航 + 资产总账，定位目标资产（勿重复盘点）。
2. 按 capability 契约执行，产出落交付目录。
3. 每步写 receipt（含 source_hash），保证可复现、可阻断（缺证据/权限即停）、可回退。
4. 发布/合并类动作停在人工审批，AI 不自动群发/合并。
5. 新决策回写 decision_log 并更新状态。

## 五、边界与红线（通用）

- 原始截图、聊天记录、内部项目数据、密钥凭证不进公开仓；私有仓也须脱敏。
- 未验证方法只能标记 candidate，不得当已验证。
- 生成 HTML / 合并 PR / 写了审稿卡 ≠ 发布完成；public_release_approved 为唯一发布批准信号。
