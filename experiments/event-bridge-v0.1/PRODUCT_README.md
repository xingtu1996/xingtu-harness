# XingTu Orchestrator（产品立项 README 草案）

> 状态：探索 / Design Preview，尚非正式发布的软件。此文档存放于 Harness 实验 PR，未来拟迁入独立产品仓库；不代表已部署任何跨平台自动编排服务。

**One Goal. Any Authorized Agent. Verified Outcomes.**

面向目标、工具中立、可验证的智能协作控制层：让用户在已有的 GPT、Muse、豆包工作、WorkBuddy、Claude Code、Codex、OpenCode 等工具环境中提出目标，借助其**确实提供、且用户授权的** API、CLI、Hook、Webhook 或文件交接方式组织任务；系统协调适合的执行能力、追踪证据，并将高风险动作留给人。

## 为什么存在

现在的一个真实任务可能经过多个 AI 客户端和本地工具，用户不得不人工复制目标、回填结果、确认版本。问题不只是调用模型，而是跨入口的目标一致性、状态可靠性、授权、回执、失败恢复和注意力成本。我们首先在自己的内容生产与 GitHub 开源矩阵上验证，再提炼外部用户可复用的模板。

## 不是

- 不是新的通用聊天客户端、模型网关、编码 Agent 或大而全的自主 Agent 平台。
- 不读取未经用户授权的聊天历史；不假设任何产品都能被自动调用。
- 不重复实现成熟的 Skill、执行器、CI、BPMN、持久化工作流和身份认证能力。
- 不以“Agent 自称完成”替代文件、测试、日志和版本证据。
- 不默认为用户合并 PR、群发文章或执行破坏性操作。

## 我们提供的差异化

1. **Goal-first**：目标、验收标准、约束与预算优先于工具入口。
2. **Bring your own agents**：接入已有模型、桌面 Agent、Coding Agent、Work Agent 与个人自动化，不迫使用户换工具或订阅。
3. **Minimal control plane**：只建设跨工具共同缺失的任务契约、授权、能力发现、状态与回执；实际执行复用成熟工具。
4. **Modes coexist**：用户目标驱动、事件驱动、定时驱动、流程/DAG/BPMN 驱动可组合，流程引擎不是唯一中心。
5. **Verified outcomes**：幂等、单写入者、回执证据、异常恢复与人工审批。
6. **Attention-aware**：默认静默，只有结果可用、异常有新证据或需人决策时通知。
7. **Cost-aware**：确定性检查优先程序实现，高能力模型只用于有收益的推理/裁决；成本收益一律实测。
8. **Portable and private**：配置模板不绑定 XingTu 目录或私有账户，敏感信息留本地或私有存储。

## 架构边界（目标，而非已实现）

Goal Interface (Chat/CLI/API/Webhook)
→ Intake / Event Bridge
→ Goal & Task Planner
→ Capability Registry + Policy Router
→ Existing Agent/Workflow Executors
→ Receipt & Evidence Store
→ Watchdog / Evaluation
→ Human Approval / Result Delivery

**Event Bridge 是实现模块，不是全部产品。** 先验证任务可靠交接与证据，再研究动态任务分解、路由和跨 Agent 恢复。接口类型需按平台逐项验证、分级声明为 native / adapter / manual / unsupported。

## 来自 DeepSeek Super Agent 的启发与引用

本项目主要参考 [DeepSeek dsh-superagent-prototype](https://github.com/deepseek-ai/dsh-superagent-prototype) 的设计哲学与实现边界：

- [000 Philosophy](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/main/docs/000-philosophy.md)：减少人的注意力占用、授权内行动、安静地工作。
- [001 Domain Model](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/main/docs/001-domain.md)：Source、Trigger、Thread、Eval、Ticket、Mandate、Assignment、Executor 的明确语义。
- [007 Architecture](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/main/docs/007-architecture.md)：Engine、Policy、Store、Outbox、执行器和单写入责任。

**引用声明**：上游明确标为 *research prototype*，不是正式 DeepSeek 产品或生产级产品；公开代码不完全等同于文章设计，一些能力尚未实现。此处是借鉴和对比，不宣称论文原创、官方合作、实现兼容或直接复刻。使用上游代码时须核对其 MIT 许可及保留署名；当前实验为独立最小实现，尚未复制上游代码。


## 与 Super Agent 的组合关系（核心设计立场）

**概念公式：Super Agent 能力体系 ≈ LLM + Harness + Event Bridge / Orchestrator（行途协同扩展）**。

这不是 DeepSeek 官方的数学定义，也不是替代或重写其 Super Agent。LLM 负责理解与推理，Harness 提供工具、Skill、执行环境和约束；行途的 Event Bridge / Orchestrator 是用于组合**已有** Super Agent 和其他工具的跨产品协作补充层，关注目标对齐、专业分工、状态交接、回执、失败恢复及权限治理。一个厂商的 Super Agent 可以作为我们的一个执行能力，也可以是用户的任务入口。

我们将基于 DeepSeek Super Agent 的设计哲学与实践持续演进，但不会宣称已经实现所有平台互通，或把其官方架构误写成由行途提出的公式。具体设计与 Mermaid 架构图见 [设计哲学](./PHILOSOPHY.md) 和 [可发布技术文章草案](./ARTICLE_DRAFT.md)。

## 与行途开源矩阵的关系

- `xingtu-harness`：安装聚合、入口和可复用工程资产。
- `xingtu-scheduled`：现有调度 Registry，未来通过适配器引用；不接管或改写历史任务。
- `xingtu-skills`：技能与能力声明来源。
- `xingtu-hooks` / `xingtu-cli`：事件采集与 CLI 接入候选。
- `xingtu-learn`：性能、模型路由、额度和失败复盘。
- `xingtu-vault`：私有真实试验田，**不是开源依赖**。

产品主仓将提出适配协议、兼容验证与跨仓 SDD；各仓保持独立，变更通过各自 PR 审核，不集中重写全部仓库。

## 第一个里程碑：Event Bridge v0.1

本 PR 下 `SDD.md`、`bridge.py`、`test_bridge.py` 是纯离线模拟。它尚不支持真实 GPT/Muse/Codex 会话直接互通、持久化、生产级租约或高并发。下一步依次为测试执行→可靠持久化→首个授权的真实适配器→模板化示例→外部用户验证。

成功标准：减少人工转述次数与单个合格成果成本；不降低质量、不重复副作用、不越过人工审批。无真实测量数据时不宣传节省比例。

## 可能的产品方向

独立开源 Starter → 可复用领域模板 → 企业/团队自托管治理与实施服务。这只是待验证的商业假设，不代表已有用户付费或成熟市场结论。
