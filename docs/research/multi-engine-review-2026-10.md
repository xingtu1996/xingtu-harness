# 多 Engine 交叉验证：业界模式、开源项目与最小可行方案

> 调研日期：2026-10-18 ｜ 调研人：Muse（研究员）
> 目标读者：行途技术（boss）——Mac + OpenCode/Claude Code 做内容创作（公众号文章、视频脚本），关心"多模型交叉评审、对抗审核"提质量，并想要 HTML 可视化界面做分发决策
> 方法：公开资料检索核验（2026-10-18），每个项目标注来源与核验状态；查不到的一律标「未核实」，不编数字

---

## 一、业界模式：四种"多 engine 验货"的路数

### 模式 1：LLM-as-a-Judge（一个模型当裁判）

- **做法**：用一个强模型按 rubric 给另一个模型的输出打分。源头是 2023 年 Zheng 等人的 MT-Bench / AlpacaEval 路线，现在是 eval 基础设施的标配。
- **已知坑**（2026 年仍成立）：裁判有立场——位置偏见（先看到的答案占优）、冗长偏见（长的显得好）、自我美化偏见；有研究称 prompt措辞微调可让模型排名翻转高达 40%（BiasScope，arXiv，检索见正文）。
- **缓解手段**：temperature=0、成对比较时交换顺序、CoT 强制说理、多次采样投票（ChainPoll）。
- **适用**：有标准答案/明确 rubric 的场景（代码、RAG 问答）。**对 boss 的文章评审：单裁判不够**——"写得好不好"没有标准答案，单裁判容易变成"裁判的口味"，这正是他要"交叉"的原因。
- **成本**：1 次 judge 调用 ≈ 1 次生成调用，token 翻倍。

### 模式 2：多智能体辩论 MAD（开庭吵架）

- **做法**：Du et al. 2023 提出——多个模型互相质疑、反驳，几轮后收敛。事实性和推理有提升。
- **代价**：token 和时间开销巨大（N 个模型 × M 轮），日常审稿用不起。
- **适用**：高风险一次性决策（架构评审、安全审计），不适合每篇文章都开庭。

### 模式 3：MARS 评审制（作者→评审→主审，最贴合 boss 的需求）

- **做法**：2026-08 论文《MARS: toward more efficient multi-agent collaboration》（Indiana University，arXiv 2026-08-24）：**作者 agent 出初稿 → 若干评审 agent 独立评审（互不交流）→ 主审（meta-reviewer）汇总做最终决定并指导修改**。
- **关键结论**：精度与 MAD 持平，**token 和时间省约 50%**——因为评审之间不互吵，省掉了最贵的那部分。
- **为什么贴合**：这正是传统出版流程（作者→外审→主编）的 AI 版，也是 boss 现有习惯（他自己当 verdict 终审）的自然延伸。**建议 MVP 直接抄这个结构**：AI 写初稿/他写初稿 → 2 个独立 AI 评审 → 他当主审拍板。
- **代码**：论文称开源在 github.com/xwang97/MARS（论文原文标注，**未实测打开**）。

### 模式 4：交叉盘问 Cross-Examination（证据倒逼认错）

- **做法**：各模型**先盲写独立结论并密封**（防跟风），再开封互相挑战——挑战必须带证据（能跑命令的 seat 用执行结果说话，不能跑的用引用），被证伪的模型要**正式认错（concede）**并留档；剩下分歧点交回给人类裁判。
- **核心洞察**：分歧是信号不是噪音——"分歧点表格"恰恰告诉你哪里需要人类判断。这句话应该刻在 boss 的看板上。
- **适用**：代码审计、日志分析、文档评审——"一个模型的自信回答不够好"的所有场景。

### 四种模式一句话选型

| 场景 | 用什么 |
|---|---|
| 每篇文章/脚本的日常审稿 | **MARS 评审制**（便宜一半，流程贴合出版习惯） |
| 关键稿件的深度挑错 | Cross-Examination（盲写+证据+认错） |
| 有标准答案的 pipeline 回归 | LLM-as-a-Judge（配 rubric + 换序） |
| 架构级高风险决策 | MAD 辩论（贵，但值得） |

---

## 二、开源项目卡（4 个，按"对 boss 的有用度"排序）

### 卡 1：CrossExam —— 协议本身就是答案 ⭐ 首选参考

- **地址**：https://github.com/cyberxuan-XBX/crossexam（2026-10-18 实测打开）
- **Stars**：7（2026-07 创建，极新、社区极小——**成熟度是最大短板**）
- **协议**：MIT
- **是什么**：零依赖单文件 Python CLI，实现"盲写密封 → 交叉盘问 → 认错/分歧表 → synthesis.md"的完整协议。三种 seat：Agentic（Claude Code / Codex CLI / Gemini CLI / aider，可执行命令验证）、API（**任意 OpenAI 兼容 endpoint**：OpenRouter、自建 vLLM、**Ollama / LM Studio 本地**）、Clipboard（网页聊天手动粘贴）。
- **OpenAI 兼容**：✅ 原生支持；本地 Ollama 一行命令即入座（`cxam seat --name qwen --endpoint http://localhost:11434/v1`）。
- **本地跑**：✅ 零依赖，bus 就是一堆本地文件，`git diff` 可看整场辩论。
- **UI**：❌ 无；输出是 `synthesis.md` + 分歧表（markdown）。**但这正是 boss 要自建 HTML 看板的原因**——协议拿来，看板自己做。
- **对 boss 的价值**：不是"拿来即用"，而是**把它的协议抄进自己的 skill**——盲写防跟风、证据倒逼、分歧表交人，这三条是审稿流程的灵魂。且它的 seat 设计天然兼容他现有的免费模型栈（GLM / AI Studio / Groq / Ollama）。

### 卡 2：Opik —— Judge 评测 + 看板的现成平台

- **地址**：https://github.com/comet-ml/opik（官方 PyPI 文档给出该 clone 地址，2026-10-18 核验）
- **Stars**：约 21,433（comet.com 2026-08-13 对比页；另有 22.4k 口径，2026-10）
- **协议**：Apache-2.0（全功能自托管免费）
- **是什么**：Comet 出的 LLM 可观测 + 评测平台。**LLM-as-a-judge 指标开箱即用**（幻觉检测、相关性等）、datasets/experiments、pytest 可进 CI。
- **OpenAI 兼容**：✅ 中立框架，SDK 接各类 provider。
- **本地跑**：✅ `docker compose up` 自托管，浏览器看 http://localhost:5173。
- **UI**：✅ 有——trace 瀑布流、评分看板、prompt 版本管理。这正是 boss 想要的"可视化"最接近的现成形态。
- **对 boss 的定位**：**重**（平台级）。不建议现在上；但它的"评分看板 + prompt 版本管理"两个设计值得抄进自建 HTML 看板。等以后稿件量大了、要沉淀评审数据时再考虑。

### 卡 3：MARS —— 论文模式，评审制的学术背书

- **地址**：论文称 github.com/xwang97/MARS（arXiv 原文标注，**未实测**）
- **协议/Stars**：未核实
- **对 boss 的价值**：不是工具，是**模式依据**——"评审制比辩论制省 50% token 且精度持平"，支撑 MVP 选 MARS 结构而不选开庭辩论。写进方案的"为什么这样设计"那一节。

### 卡 4：AI Devil's Advocate（LangGraph + Streamlit，有 UI 的实例）

- **地址**：GitHub 仓库链接见 dev.to 原文（https://dev.to/humam_moin/building-an-ai-devils-advocate-a-multi-agent-debate-app-with-langgraph-streamlit-ai-53mo），**仓库具体地址未核实**；另有在线 demo。
- **Stars/协议**：未核实
- **是什么**：2026-10-11 的个人项目——正方/反方两个 agent 辩论 + 裁判 AI 给结构化 verdict；**provider 在 Groq / Gemini / OpenRouter 之间切换，429 自动 fallback**；Streamlit UI（辩手卡片、动画）、辩论导出 PDF/Markdown、侧栏实时 API 调用计数器。
- **对 boss 的价值**：**UI 概念验证**——"免费 tier 拼多家 + 自动 fallback + 可视化看板"这条路有人跑通了，且用的正是他现有的免费栈。fallback 工
...[truncated 11781 chars]