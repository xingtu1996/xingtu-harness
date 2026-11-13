# XSA · XingTu Super Agent

> Research Preview · 目标驱动、工具中立、专业协作。当前是设计和离线原型，不是可直接连接所有 Agent 的生产系统。

**One Goal. Many Agents. Verified Outcomes.**

XSA extends existing LLM and Harness ecosystems with event-driven coordination, capability routing, scheduled workflows, execution receipts, watchdog monitoring, and human-in-the-loop governance.

XSA 是面向目标的开放式 Super Agent 协作系统。参考 DeepSeek Super Agent 的设计哲学，复用 GPT、Muse、豆包工作、WorkBuddy、OpenCode、Claude Code、Codex 等已有能力，并在授权接口可用时以统一任务、事件、状态和回执协调执行。

## 为什么做

一次真实目标经常跨越 Chat → GitHub → Coding/Work Agent → GitHub → 审核 → 再执行。用户被迫充当消息队列、任务调度器和审核控制器。XSA 优先解决人工交接、版本丢失、重复执行、假成功、成本不可见和授权边界。

## 设计模型

**Super Agent 能力体系 ≈ LLM + Harness + XSA 协同编排扩展。**

这是行途的工程理解，不是 DeepSeek 官方公式；并不替代 DeepSeek Super Agent。现成 Super Agent 可作为入口或专业执行器，XSA 主要提供跨产品协作的补充控制层。

## 核心能力规划（非全部已实现）

| 能力 | 状态 |
|---|---|
| Task / Event / Receipt 协议 | 离线原型 |
| 模拟 Muse / Codex 路由 | 离线原型 |
| Event Bridge、重复事件去重 | 离线原型 |
| Watchdog 异常发现 | 模拟 |
| 持久化队列、租约和恢复 | 待实现 |
| 授权的真实 GitHub 适配器 | 待验证 |
| 外部 Agent API/CLI/Hook 适配器 | 按产品逐一验证 |
| BPMN/DAG/定时驱动 | 设计阶段 |
| Token 和质量 A/B 基准 | 待实测 |

## 结构与治理

- `docs/`：哲学、架构、ADR、路线图、引用
- `src/xsa/`：核心协议、策略与执行适配器
- `adapters/`：经验证的各产品接入
- `tests/`：幂等、权限、安全与失效恢复
- `examples/`：不依赖私有环境的可运行示例
- `templates/`：默认只读、默认 dry-run 的安装模板
- `.github/`：Issue/PR 模板、CI 与安全门禁

## 首个实验

最小链路：一条目标 → 模拟 Muse / Codex Worker → 回执 → Watchdog → 人工审批。原型与测试来源：[xingtu-harness Event Bridge PR #4](https://github.com/xingtu1996/xingtu-harness/pull/4)。

## 上游致谢与参考

- [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness)：Everything is a Plugin、插件化工程结构与开源治理。
- [DeepSeek Super Agent 研究原型](https://github.com/deepseek-ai/dsh-superagent-prototype)：Source / Trigger / Mandate / Executor、执行与回执、减少人类注意力。
- [Super Agent 架构](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/main/docs/007-architecture.md)。

不是官方合作、官方衍生版本或完整兼容声明。使用上游实现代码前需单独检查许可证和署名义务。

## 安全边界

不读取未经授权的聊天数据，不转存密钥，不假定订阅额度可共享；不自动合并 PR、不自动群发、不执行未经授权的破坏性操作。

## 许可证

拟采用 MIT；独立仓创建时需正式加入 LICENSE，并核对所有引用依赖的许可证。未添加许可证前不要声称新仓已经获得 MIT 授权。
