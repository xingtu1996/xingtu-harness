# 行途 Event Bridge v0.1｜实验 SDD

> 状态：实验草案；2026-11-02。只允许离线模拟，不接入任何现有生产任务。
> 定位：把“人工复制 GPT ⇄ Muse ⇄ Codex 对话”变为“结构化任务、授权执行、可验证回执”。不声称直接读写任意聊天应用。

## 价值与边界

- 入口不限于 GPT/Muse/Grok/豆包工作/WorkBuddy；前提是平台提供**已获授权**的 API、CLI、Webhook，或用户主动导出的文件交接。
- 没有接口的平台只提供手工提交任务包适配器；不能冒充实现了全自动双向会话。
- 默认由确定性规则进行路由，不为 heartbeat、SHA 检查和去重调用大模型。
- Muse 适合资料和内容生产，Codex 适合代码与测试，GPT 适合跨领域评审，最终发布与高风险变更保留人工审批。
- Event Bridge 管任务控制平面，不替代 xingtu-scheduled 任务登记，不改 xingtu-vault 发布流程。

## 最小任务协议

Task：task_id（唯一）、objective、kind、input_revision、owner、approval_required、state、created_at、updated_at。
Event：event_id、task_id、kind、input_revision、created_at、payload_ref（指向脱敏输入，不传原始聊天）。
Receipt：task_id、event_id、worker、status、output_ref、evidence_sha、error_code、completed_at。

事件需先去重；幂等键 = task_id + kind + input_revision。真实系统须用数据库唯一约束或事务式条件更新。不能用仅靠 JSON 文件覆盖的抢锁实现生产多 Worker 互斥。

## 状态机

`queued -> leased -> succeeded | failed | approval_required`。
`leased -> expired` 仅表示需要调查，不得立即双跑。
`failed/expired -> queued` 需要在回收旧租约、验证副作用并满足重试预算后执行。
外部发布、合并 PR、删文件一律须单独授权，状态转换不是授权。

## Watchdog

检查 heartbeats、租约过期、产物日期/大小、回执引用及输入 SHA；对相同异常按 fault_key 去重。状态恶化、证据更新或有新人工动作时才重新提醒。证据不可读标 unverified，不推断 failed。

## 验证任务

- T1：一条 content 任务由模拟 Muse Worker 接收，留存回执；重复 event 不二次执行。
- T2：一条 code_review 任务由模拟 Codex Worker 接收，回执与输入 SHA 对应。
- T3：故障模拟（重复消息、失败、超时、权限不足）不重复产生副作用，异常可以被监控发现。

## 开源模板要求

适配器按能力声明：available / authorization / permissions / quota / actual_transport。禁止默认读取聊天记录。安装默认 dry_run=true、publish=manual、merge=manual，配置采用示例占位符；敏感任务与证据保留私有仓。外部开源用户不依赖 XingTu 路径和额度。

## 研究引用及限制

- DeepSeek 官方研究原型：https://github.com/deepseek-ai/dsh-superagent-prototype
- 官方架构说明：https://github.com/deepseek-ai/dsh-superagent-prototype/blob/main/docs/007-architecture.md
- GitHub Actions 触发：https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows
- GitHub repository_dispatch：https://docs.github.com/en/rest/repos/repos#create-a-repository-dispatch-event

仅将 DeepSeek 材料称为“设计与开源原型”；未核实正式同行评审论文、DOI，不把原型描述为生产级框架，也不把功能接口设计当成已可调用平台。

## 阶段验收

T1–T3 各至少连续成功 3 次、重复副作用 0、未授权外发 0。记录 input/output 版本、人工交接次数、真实 token/cost、执行时长和独立质量评分。没有真实计量时标“待测”，不得推断节省百分比。后续生产接入需单独安全审核、租约持久化与权限治理 PR。
