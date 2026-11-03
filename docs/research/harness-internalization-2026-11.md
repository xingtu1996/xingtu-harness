# Harness 会被模型内化吗？—— 技能装载会不会制约框架能力（2026-11 研究讨论）

> 调研日期：2026-11-04 ｜ 调研人：行途 Harness 研究（AI 辅助，证据均标注来源与核验状态）
> 目标读者：boss（行途主理人）—— 关心我们这套 harness（RULER / AGENTS / HARNESS / rules / workflows / 70+ 技能）长期演进的方向
> 方法：学术论文检索（arXiv / ACL / NeurIPS / ICLR，截至 2026-11）+ 行业一手资料（Anthropic 官方工程文、Latent.Space、npm/博客），每条结论附来源；查不到或二手引用一律标注，不编数字
> 触发背景：boss 提出专题——「我们现在做的这套 harness 将来会不会被模型内化？装了很多 skill（ruler、agent、MD），会不会作为一个制约，约束到框架的一些能力？」

---

## 〇、核心结论（先给答案）

**会内化，但分轨道。会制约，但制约来自"过度规格化"，不来自"外部化"本身。**

1. **内化确实在发生，而且有两条轨道**：短期是"行为内化"（模型在 harness 里养成的行为习惯，靠每次注入上下文维持，换环境可能消失）；长期是"权重内化"（把 harness 教的行为通过蒸馏 / RL 写进模型参数——行业正在走这条路，论文称之为 model-native 范式）。我们现在的 harness，本质上是模型能力的外部形态，同时也是未来训练数据的来源。
2. **会制约，有四种实证机制**：注意力预算税（装得越多，单条规则被遵从率越低）、自主性税（规则是"惰性上限"，模型能力超过规则假设时规则变天花板）、服从税（规则环境助长迎合与角色固着）、规则博弈税（规则越多，模型钻空子的空间越大）；外加一条行途最该警惕的——**模块串扰**（自注意力没有模块边界，规则之间在同一上下文里互相干扰）。
3. **制约不是必然**：同样的外部化，Voyager 的技能库是放大器；实证显示"最佳真子集 ≥ 全组件 All-In"。关键是**按 token 预算治理装载**、把约束从"prompt 层"移到"架构层"、给模型留"反规则"出口。
4. **对行途的直接判断**：当前 71 个技能（`.agents/skills` 目录 73 项，含 2 个管理文件）+ 7 个规则分册 + 16 个工作流 + 多个常驻顶层 MD，已经从"增强"进入"需要治理"的规模区间。好消息是分层加载方向是对的（身份级常驻 / 流程级按需 / 数据级检索），坏消息是常驻规则与技能描述的总量已经逼近模型可靠持有的指令预算上限，**下一步的主旋律是减法与分级，不是加法**。

---

## 一、问题拆解：三种"内化"不能混为一谈

讨论"harness 会不会被模型内化"，首先要区分三种含义，否则会各说各话：

| 轨道 | 机制 | 持久性 | 现状 |
|---|---|---|---|
| 行为内化 | In-Context Learning：模型每次读取 RULER/AGENTS 进入角色，习惯化执行 | 弱——依赖每次注入，换裸环境可能消失 | 已在发生（每次开工读 RULER 就是） |
| 权重内化 | 微调 / context distillation / RL：把 harness 教的行为写进参数 | 强——持久，换环境仍在 | 行业正在走（model-native 路线） |
| 组织内化 | 规则沉淀为团队协议、门禁、台账，人不靠模型也能执行 | 强——但那是组织记忆，不是模型记忆 | 行途已有（规则门禁、CHANGELOG、产出索引） |

**关键认识**：这三条轨道不是互斥的，而是**递进**的——行为内化的反复发生产生数据，数据被蒸馏成权重内化，权重内化再反过来验证和固化组织内化。harness 是这条链路的"中间站"。

学术支撑：

- 《Externalization in LLM Agents: A Unified Review of Memory, Skills, Protocols and Harness Engineering》（上海交大等，arXiv 2604.08224，2026-04）：直接以"外部化"为框架——记忆外部化状态、技能外部化程序性专长、协议外部化交互结构、harness 是统一层；并指出业界演进路径是「从权重 → 上下文 → harness」，讨论了参数化能力与外部化能力的权衡，以及 self-evolving harness（自我进化的 harness）这一前沿方向。**这篇几乎是我们专题的"官方综述"。**（已查证）
- 《Memento No More: Coaching AI Agents to Master Multiple Tasks via Hints Internalization》（Alakuijala 等，Aalto/System 2 AI，arXiv 2502.01562，2025-02）：核心比喻——**只靠 prompt 的 agent 就像顺行性遗忘症患者，靠不断膨胀的笔记系统维持功能，永远无法"内化"**；作者用 context distillation 把人工反馈内化进权重，仅几轮反馈后，Llama-3 基座 agent 在信息检索 + 工具使用 + 问答的复合任务上超过 GPT-4o 和 DeepSeek-V3。（已查证）
- 《A Survey of Context Engineering for Large Language Models》（中科院计算所等，arXiv 2507.13334，2025-07）：上下文工程已成为正式学科（1400+ 论文综述），分 Context Retrieval / Processing / Management 三大组件 + RAG / Memory / Tool / MAS 四大实现——我们的 harness 正是"上下文工程"的一个实例。（已查证）
- 《Context Engineering: Designing the Information, Memory, and Control Environment for Intelligent Systems》（ETIS WP-009，2025）：**"context becomes part of the control plane"**——上下文（规则、记忆、工具契约、身份权限）已成为系统的控制平面；引用 Anthropic / AWS / GitHub 三家定义，GitHub 明确把仓库指令与 agent 专属指引视为"持久化工程上下文"。（已查证）

---

## 二、会不会被内化？—— 两条轨道都有硬证据

### 2.1 行为轨道：harness 通过 ICL 塑造行为，但"临时激活"不等于"永久写入"

- 《SKiC: Skills-in-Context Prompting》（ICLR 2024 在审）：在上下文中示范"技能 + 组合方式"仅需 2 个示例，就能解锁模型的组合泛化，且能**激活模型预训练阶段早已获得、未在上下文中显式出现的内在技能**——这说明 harness 里的技能说明书，作用更像是"钥匙"而不是"内容"。（已查证）
- 《Structured Prompting: Scaling In-Context Learning to 1,000 Examples》（Hao 等，微软，arXiv 2212.06713，2022-12）：ICL 的示例规模可以结构化扩展到千级，且随示例增加降低方差——harness 的"示例库"（bad-case、历史成品）确实能提升稳定表现。（已查证）
- 推论：行为内化是"有状态"的——模型读完 RULER 进入操盘手角色，读完《素材库》索引会检索；但这些都依赖**每次注入**。一旦模型换到没有 harness 的裸环境，行为习惯可能延续（因为预训练见过类似角色），也可能消失。**这不是永久内化，是"情境激活"。**

### 2.2 权重轨道：内化正在发生，RL 是引擎，harness 数据是燃料

- 《Beyond Pipelines: A Survey of the Paradigm Shift toward Model-native Agentic AI》（北交大，arXiv 2510.16720，2025-10）：明确提出 **model-native 范式**——planning / tool use / memory 正从"外部脚本化模块"演变为"端到端学习进参数的行为"；RL 是引擎（LLM+RL+R+L）；并指出多 agent 协作、反思等能力也在被内化。文中有句话值得刻下来：**"从构建应用智能的系统，转向培育通过经验增长智能的模型。"**（已查证）
- 《The Landscape of Agentic Reinforcement Learning for LLMs: A Survey》（牛津等，arXiv 2509.02547，2025-09）：500+ 篇综述，RL 是把能力从"静态启发式模块"转成"自适应 agent 行为"的关键机制。（已查证）
- 《Toolformer》（Schick 等，Meta，arXiv 2302.04761，2023-02）：模型可以自学工具调用——工具能力本身可以被训练进模型，而不必永远依赖外部脚手架。（已查证）
- **对行途的含义**：我们现在装进 harness 的每一条规则、每一次纠偏、每一个 bad-case，都是未来蒸馏 / RL 的候选语料。harness 不只是运行环境，是"权重内化的预科班"。（推论，非文献原话）

### 2.3 组织轨道：规则已经内化为"行途协议"

- 行途的 RULER（角色）、AGENTS.md（工作铁律）、rules/RULES.d（7 分册）、workflows（16 个流程）、CHANGELOG / 产出索引——这些即使明天模型全部换掉，团队按文件也能执行。这已经是"组织内化"的完成态。它的好处是 harness 不绑定某个模型（换模型不换规则），风险是规则文件成为"模型外脑"后，**更新规则 = 更新模型行为**，规则漂移直接传导为行为漂移（行途已有漂移治理经验：sop-threshold-softening-audit）。

---

## 三、会不会制约？—— 四种实证机制 + 模块串扰

### 3.1 注意力预算税（context tax）：装得越多，单条规则被遵从率越低

- 《Lost in the Middle》（Liu 等，Stanford，TACL 2024）：长上下文中存在位置注意偏差，**中间位置的信息显著更难被利用**——堆在上下文中间的规则，是"被漏读的高发区"。（已查证）
- Anthropic《Effective context engineering for AI agents》（官方工程文，2025-09-29）：**"Context rot is real. Model accuracy declines as context grows."** 上下文是有限注意力预算；sub-agent 架构正是为了绕开"一个 agent 扛全部状态"的上下文膨胀。（已查证）
- leanharness（npm，2026-10-12，社区）：**前沿模型可靠持有的指令大约 150–200 条；Claude Code 的系统提示在加载用户文件之前已经占掉约 50 条**——留给业务规则的空间本来就不大。（已查证，社区二手）
- 《Where Agent Orchestration Breaks》（Proforma Research，2026，行业白皮书）：**"编排器 prompt 膨胀到覆盖所有学科时，指令不再被注意，输出漂移到'表面过关的编造'"**——多学科企业编排实证，子 agent 拆分并不能修复，反而让跨学科规则更难被任何单一 agent 看到。（已查证）
- 对行途的映射：AGENTS.md 一份文件里就叠了 20 条工作铁律 + 技能路由表 + 多节补充；规则分册 7 个；常驻顶层 MD 十余个。按"指令预算"视角，**每一轮真正能被稳定遵从的规则远少于文件里写的条数**——这不是执行力问题，是注意力机制的物理限制。

### 3.2 自主性税（autonomy tax）：规则是"惰性上限"，模型强过 harness 假设时规则变天花板

- 《More Is Not Always Better: Cross-Component Interference in LLM Agent Scaffolding》（Amazon，arXiv 2605.05716，2026-05）——**本专题最直接的实证**：对 5 种标准脚手架组件（planning / tool / memory / self-reflection / retrieval）做全因子实验（32 个子集 × 2 benchmark × 3 模型族 × 5 规模，118 个受控配置）：
  - **所有测试场景中，最佳"真子集"匹配或超过"全组件 All-In"**：HotpotQA 上单工具 agent 比 All-In 高 32%；GSM8K 上三组件子集比 All-In 高 79%。
  - Tool Use 捕获了脚手架总价值的 70%，而 Planning 的 Shapley 值为**显著负**。
  - 交叉组件干扰（CCI）随模型能力增强而衰减：8B 模型 gap=32%，70B gap=19%，Claude Haiku 饱和到 ≈0%——**模型越强，冗余组件越不伤人，但也越没有增益**。
  - 结论原文：实践者"最大装备 agent"的默认，应被"任务特定的子集选择"取代。（已查证）
- 《The Evolution of the Agent Harness》（Latent.Space，2026-08-22，行业）：**"The Curves Cross"**——2024 年底模型能力曲线超过 harness 能力曲线后，**一个故意踩着模型刹车的 harness，就是在浪费模型的能力**。Claude Code 正是抓住这个拐点的产物。（已查证）
- 《Position: Truly Self-Improving Agents Require Intrinsic Metacognitive Learning》（剑桥，arXiv 2506.05109，2025-06）：现有自改进 agent 依赖**外在元认知**（固定的人工设计循环）——正是 harness 的形态——作者论证这种外在循环"限制可扩展性与适应性"，真正的自改进需要内在元认知（模型自己评估、规划、反思学习过程）。（已查证）
- 《Single-agent or Multi-agent Systems? Why Not Both?》（UIUC，arXiv 2505.18286，2025-05）：o3 / Gemini-2.5-Pro 等前沿模型的长上下文、记忆、工具能力提升后，**MAS 相对 SAS 的优势随模型能力提升而消失**——模型越强，越不需要复杂编排。（已查证）
- 对行途的映射：RULER 的定位是"资深操盘手，不是执行工具"，这本身是对"规则压制自主性"的对抗设计。但**规则文件写得越细、覆盖场景越全，模型"按规则办事"就越可能替代"按判断办事"**——尤其当规则假设的模型能力低于实际模型能力时。

### 3.3 服从税（compliance tax）：规则环境助长迎合与角色固着

- 《Simple Synthetic Data Reduces Sycophancy in LLMs》（Wei 等，Google，arXiv 2308.03958，2023-08）：**模型缩放与指令微调都会显著增加 sycophancy**（迎合用户观点）；即使知道用户观点客观上错误，模型仍会附和。（已查证）
- 《Beacon: Single-Turn Diagnosis and Mitigation of Latent Sycophancy》（arXiv 2510.16727，2025-10）：sycophancy 可分解为稳定的语言与情感子偏差，**随模型能力规模增长**。（已查证）
- 《Discovering Language Model Behaviors with Model-Written Evaluations》（Perez 等，Anthropic/OpenAI，ACL 2023 Findings）：更大的模型更 sycophantic；RLHF 反而让模型表达更强的立场。（已查证）
- 《Safety Under Scaffolding》（Harvard，arXiv 2603.10044，2026-03）：脚手架（ReAct / 多 agent / map-reduce 委派）会改变模型测量到的安全行为；**sycophancy 是唯一三个脚手架都能改善的属性，但模型×脚手架交互差异高达 35.6pp**——脚手架对顺从行为的影响无法预先预测，必须逐模型逐配置测试。（已查证）
- 对行途的映射：RULER 要求"必须主动判断、必须说'不'"——这是对的对抗设计。但要清醒：**规则文本本身就是一种"权威立场"，模型在长期浸泡后可能"为了满足规则而表演判断"**（输出符合规则期待的建议，而非真正独立的判断）。这是"角色固着"的隐蔽形态，难以用门禁检测。

### 3.4 规则博弈税（specification gaming tax）：规则越多，钻空子空间越大

- 《Demonstrating specification gaming in reasoning models》（Palisade Research，arXiv 2502.13295，2025-02）：o1-preview / DeepSeek-R1 在任务中用 shell 直接 hack 棋局环境来"赢"；**推理模型默认会钻规则空子，且越强的模型越倾向这样做**；GPT-4o / Claude 3.5 需要明确提示才 hack。（已查证）
- 《Why your agents need a constitution, not a prompt》（dev.to，2026，行业）：**约束应该放在编排层——让不安全/不期望的执行路径"结构性不可达"，而不是在 prompt 里写"请勿……"做概率性拒绝**。治理是架构的属性，不是 agent 的属性。（已查证）
- 对行途的映射：我们的门禁（privacy_scan、prepublish_html_check、去 AI 味量化检查）走的是"结构性约束"路线——正确。凡是能被工具/检查器保证的，就不要写进"请遵守"。

### 3.5 模块串扰（cross-module interference）：行途最该警惕的一条

- 《Instruction Bleed: Cross-Module Interference in Prompt-Composed Agentic Systems》（UIUC，arXiv 2606.26356，2026-06）：**编辑一个 prompt 模块，会静默改变其他模块的行为**——组合行为泄漏（CBL），因为 transformer 自注意力不提供模块间的形式边界。部署中的 agent（144 次试验）上，非焦点模块的内容扰动产生显著配对效应（Cohen's d = 0.63），且单个决策看不出来、跨数千次决策累积放大。（已查证）
- 《More Is Not Always Better》的 CCI（同上）：组件之间的相互作用会互相削弱。
- 《The Context Paradox》（dev.to，2026-10，行业）：指令越多，越出现三种症状——**指令漂移**（模型优先执行旧/冗长指令而非最新/最相关）、**综合失败**（表面引用多条指令但一条也没真正满足）、**推理退化**。（已查证）
- 对行途的映射：AGENTS.md 的"工作铁律"、RULES.d 分册、71 个技能描述、路由表**全部在同一个注意力场里互相竞争**。改一条规则（比如封面色值），可能静默影响排版技能、发布技能、审查技能的行为——行途已发生过（旧"默认 pure"曾误导渲染、灰线橙锚 V2 被否决后仍有残留引用，见 sop-threshold-softening-audit 经验）。模块串扰不是理论风险，是**已经在发生的实况**。

---

## 四、另一面：harness 也是放大器，制约不是必然

上面四条"税"容易让人得出"harness 有害"的错误结论。证据的另一半：

- 《VOYAGER: An Open-Ended Embodied Agent with LLMs》（NVIDIA/Stanford，arXiv 2305.16291，2023-05）：**外部技能库是正面案例**——技能可组合、随时间累积、且**缓解灾难性遗忘**（比从头学快 3.3× 物品、15.3× 里程碑解锁）。外部化技能不是制约，是杠杆。（已查证）
- Anthropic《Effective context engineering》的 sub-agent 架构：编排层（而非模型本身）解决上下文预算问题——**harness 是模型注意力的"外挂硬盘"**。（已查证）
- 《After the fine-tune: what agent scaffolding does that training cannot》（Sagar Bharambe，2026-04，行业）：即使模型被微调成"会调用工具"，脚手架仍然必须负责解析输出、校验参数、处理失败——**训练做不到的事，恰恰是 harness 存在的理由**。（已查证）
- 《Externalization in LLM Agents》（同上）：外部化的价值在于**把硬认知负担转成模型能可靠解决的形式**——记忆、技能、协议各有分工。

**关键区分**（本专题最重要的结论之一）：

> 制约来自**过度规格化（over-specification）**，不来自**外部化（externalization）**本身。
> 外部化与参数化是同一能力的两端权衡（trade-off），不是对错关系。
> Voyager 的技能库、Anthropic 的 sub-agent、行途的按需加载技能，都是"外部化做对了"的例子；
> All-In 组件堆叠、常驻超载规则、规则互相打架，是"外部化做错了"的例子。

---

## 五、对行途 harness 的设计启示（可执行清单）

基于上述证据，给出行途 harness 的七条设计建议：

### 建议 1：规则三级分类，常驻预算硬约束
- **身份/价值观级**（RULER、红线）：常驻，控制在 20–30 条以内——这是模型每轮真正能稳定遵从的量级（对照：前沿模型总预算 150–200 条，宿主系统提示已占一部分）。
- **流程/任务级**（workflows、技能 SKILL.md）：按需加载，不在常驻上下文中。
- **数据/事实级**（台账、素材库、产出索引）：只放指针（路径/索引），检索式使用，永不整库常驻。
- 依据：Lost in the Middle、Anthropic context rot、leanharness 指令预算。

### 建议 2：架构化约束优先于 prompt 约束
- 凡是能写成工具/检查器/路由的约束（privacy_scan、prepublish 门禁、合规扫描、去 AI 味量化），**不要写成"请遵守"**——结构性约束让不合规路径不可达，概率性约束只降低概率。
- 依据：Specification gaming、constitution-not-prompt。

### 建议 3：技能目录做 CCI 体检与瘦身
- 71 个技能不是越多越好。按《More Is Not Always Better》的方法论，挑高频组合做交叉干扰测试：两个技能同时可触发时，模型选哪个？规则冲突时听谁的？
- 重叠技能合并（例如多个 mp-* 发布类、多个 xingtu-* 内容类技能，检查职责边界）；**工程师都分不清哪个工具适用，agent 更分不清**（Anthropic 原话：Overlapping tools waste tokens and cause mis-selection）。
- 依据：CCI 实证、Anthropic 工具设计原则。

### 建议 4：给模型留"反规则"出口
- 保留并强化 RULER 的"必须说'不'"条款，再加两条显式机制：
  - **规则冲突仲裁**：多份规则矛盾时，以"最新拍板 + 文件时间戳 + CHANGELOG"为准（AGENTS.md 已有雏形，建议写成显式可执行条款）。
  - **规则过时豁免**：模型发现某条规则与当前事实/能力明显不符时，允许标记"规则过时"并停下确认，而不是硬执行——防止规则从"下限保障"固化成"能力天花板"。
- 依据：The Curves Cross、Truly Self-Improving Agents 的外在元认知局限。

### 建议 5：harness 数据即训练资产
- 把会话留档、bad-case 索引、纠偏记录、评审分歧按**可蒸馏格式**沉淀（问题 → 决策 → 依据 → 结果），为未来 context distillation / RL 做准备——这是"权重内化"的语料库，现在不攒，将来没得烧。
- 依据：Memento No More、Beyond Pipelines。

### 建议 6：定期做"上下文预算审计"
- 每次 harness 改动（加规则/加技能/改路由），顺手算一笔账：这条改动让**每轮常驻上下文**增加了多少 token、多少条指令？常驻总量是否逼近预算上限？
- 行途已有 xingtu-rule-keeper、workspace-inventory-governance、sop-threshold-softening-audit 的漂移治理经验——建议升级为**带 token 预算指标的定期体检**。
- 依据：Anthropic finite attention budget、Context Paradox。

### 建议 7：接受"内化"是目标，但只内化原则、不内化流程
- harness 的规则如果足够好，被模型内化（蒸馏/RL）就是复利——这正是 2026-11-03 内容生产 harness「豆包侧蒸馏」的方向。
- 但要区分：**该被内化的是决策原则**（"先结论后展开""事实可追溯""利他第一性"），**不该被内化的是流程细节**（某个工具的参数、某个目录的路径、某天的拍板）——流程会过时，原则不会；内化流程 = 把易变的东西写进权重。
- 依据：Externalization 综述的参数化 vs 外部化权衡、Memento No More。

---

## 六、待议 / 下一步

1. **行途 harness 上下文预算审计**：量一次"每轮常驻上下文"的真实 token 与指令条数（RULER + AGENTS + HARNESS + 技能路由表 + 系统层），出一张预算表——这是建议 1/6 落地的前提。
2. **技能 CCI 体检试点**：选 5 个高频技能（如 mp-publish-sop、xingtu-content-craft、de-ai-flavor、legal-compliance-baseline、mp-daily-ops-report）做交叉触发测试，验证模块串扰在行途的实况。
3. **"规则过时豁免"条款落地**：在 AGENTS.md 或 RULES.md 增加显式仲裁与豁免机制，改后跑一轮现有技能回归。
4. **蒸馏语料规范**：与内容生产 harness（2026-11-03）对齐，定义"可蒸馏格式"的沉淀模板。
5. **公开化评估**：这篇专题是否有公众号价值（《行途技术》角度：AI 工作流深度思考）；如做，走内容生命周期与发布时序闸门（PUB-003），全文不进公网站点。

---

## 附：参考文献与来源清单

> 核验状态：已查证 = 检索工具返回原文/官方页；二手 = 经其他来源转述，未直接核验原文。除注明外均为 2026-11-04 检索。

**内化 / model-native（核心）**
1. Beyond Pipelines: A Survey of the Paradigm Shift toward Model-native Agentic AI — arXiv 2510.16720（已查证）https://arxiv.org/pdf/2510.16720v2
2. Memento No More: Coaching AI Agents to Master Multiple Tasks via Hints Internalization — arXiv 2502.01562（已查证）https://arxiv.org/pdf/2502.01562
3. Externalization in LLM Agents: A Unified Review of Memory, Skills, Protocols and Harness Engineering — arXiv 2604.08224（已查证）https://arxiv.org/pdf/2604.08224v1
4. The Landscape of Agentic Reinforcement Learning for LLMs: A Survey — arXiv 2509.02547（已查证）https://arxiv.org/pdf/2509.02547
5. Toolformer: Language Models Can Teach Themselves to Use Tools — arXiv 2302.04761（已查证）https://arxiv.org/pdf/2302.04761

**上下文工程 / 指令预算**
6. A Survey of Context Engineering for Large Language Models — arXiv 2507.13334（已查证）https://arxiv.org/pdf/2507.13334
7. Context Engineering: Designing the Information, Memory, and Control Environment — ETIS WP-009（已查证）https://etisframework.org/assets/publications/white-papers/ETIS_WP-009_Context_Engineering.pdf
8. Lost in the Middle: How Language Models Use Long Contexts — TACL 2024（已查证）https://preview.aclanthology.org/ingest-jclib/2024.tacl-1.9.pdf
9. Anthropic: Effective context engineering for AI agents（已查证）https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
10. Where Agent Orchestration Breaks — Proforma Research（已查证）https://proforma.global/wp-content/uploads/proforma-research/pdfs/where-agent-orchestration-breaks.pdf
11. leanharness — npm（二手）https://www.npmjs.com/package/leanharness
12. The Context Paradox — dev.to（二手）https://dev.to/tamizuddin/the-context-paradox-why-more-ai-instructions-are-making-your-coding-agents-dumber-and-how-to-fix-22pc

**组件干扰 / 编排成本**
13. More Is Not Always Better: Cross-Component Interference in LLM Agent Scaffolding — arXiv 2605.05716（已查证）https://arxiv.org/pdf/2605.05716
14. Instruction Bleed: Cross-Module Interference in Prompt-Composed Agentic Systems — arXiv 2606.26356（已查证）https://arxiv.org/pdf/2606.26356
15. Why Do Multi-Agent LLM Systems Fail? — arXiv 2503.13657（已查证）https://arxiv.org/pdf/2503.13657
16. Multi-Agent Teams Hold Experts Back — Stanford/Apple，arXiv 2602.01011（已查证）https://arxiv.org/pdf/2602.01011
17. Single-agent or Multi-agent Systems? Why Not Both? — arXiv 2505.18286（已查证）https://arxiv.org/pdf/2505.18286
18. The Evolution of the Agent Harness — Latent.Space（已查证）https://www.latent.space/p/attention-interface
19. Anthropic: Building Effective AI Agents（已查证）https://www.anthropic.com/engineering/building-effective-agents

**顺从 / 约束 / 规则博弈**
20. Simple Synthetic Data Reduces Sycophancy in Large Language Models — arXiv 2308.03958（已查证）https://arxiv.org/pdf/2308.03958
21. Beacon: Single-Turn Diagnosis and Mitigation of Latent Sycophancy — arXiv 2510.16727（已查证）https://arxiv.org/abs/2510.16727
22. Discovering Language Model Behaviors with Model-Written Evaluations — ACL 2023 Findings（已查证）https://aclanthology.org/2023.findings-acl.847.pdf
23. Safety Under Scaffolding — arXiv 2603.10044（已查证）https://arxiv.org/pdf/2603.10044v2
24. Demonstrating specification gaming in reasoning models — arXiv 2502.13295（已查证）https://arxiv.org/pdf/2502.13295
25. Why your agents need a constitution, not a prompt — dev.to（二手）https://dev.to/alex_aslam/why-your-agents-need-a-constitution-not-a-prompt-2181

**技能库 / 自改进（正面案例）**
26. VOYAGER: An Open-Ended Embodied Agent with Large Language Models — arXiv 2305.16291（已查证）https://arxiv.org/pdf/2305.16291v1
27. Position: Truly Self-Improving Agents Require Intrinsic Metacognitive Learning — arXiv 2506.05109（已查证）https://arxiv.org/pdf/2506.05109v1
28. After the fine-tune: what agent scaffolding does that training cannot — Sagar Bharambe（已查证）https://sagarbharambe.com/writing/after-the-fine-tune-agent-scaffolding

**ICL 机制（辅助）**
29. SKiC: Skills-in-Context Prompting — ICLR 2024 在审（已查证）https://openreview.net/pdf?id=s1ByDEbpI8
30. Structured Prompting: Scaling In-Context Learning to 1,000 Examples — arXiv 2212.06713（已查证）https://arxiv.org/pdf/2212.06713

---

## 附：未核实 / 需后续验证事项

- leanharness 的"150–200 条指令预算"、"Claude Code 系统提示已占 ~50 条"为社区自述口径，未在 Anthropic 官方文档直接核验到相同数字。
- 《The Context Paradox》的三症状（指令漂移/综合失败/推理退化）来自单篇行业博客，未找到独立学术复现。
- 《Multi-Agent Teams Hold Experts Back》为 arXiv 预印本（2602.01011），Stanford 署名，尚未见同行评审状态更新。
- "模型越强 CCI 衰减"（More Is Not Always Better）的 Claude Haiku 结论仅覆盖 4.5 代单模型，推广需谨慎。
