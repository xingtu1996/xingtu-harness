# 免费模型接入 OpenCode / Claude Code 使用路径

> 整理日期：2026-10-18 ｜ 适用：Mac + OpenCode / Claude Code
> 结论全部经官网/官方文档核验（2026-10-18），来源见文末；无法核验的一律标注。

## 0. 背景：免费去哪了

- OpenCode Zen 免费 tier 自 2026-09 收紧：**每天 200 requests**，14 个模型轮换，**仅限 App 内调用**（CLI 会报 `Free tier can only be used from within OpenCode`），且多数免费模型会拿你的 prompt 做训练。
- "DeepSeek with Flash" = **DeepSeek V4.1 Flash Free**（Zen 名单里的那一个）；"Gemini M5 with Flash" 查无此模型，不用再找。
- **已死**：GitHub Models 于 2026-07-30 完全退役；Cerebras 无常驻免费（仅 $5 试用）；DeepSeek / MiniMax / Kimi 官方均无免费 tier。

## 1. 按密级分流（三条线，先看这张表）

| 密级 | 走什么 | 说明 |
|---|---|---|
| 🔴 涉密（身份证号、财务、未公开商业信息、客户代码） | **只走本地 Ollama**（第 3 节） | 数据不出本机，无例外 |
| 🟡 一般工作文档、公开创作素材 | 智谱 GLM（首选）、Groq、Zen 免费 | 注意免费 tier 训练条款 |
| ⛔ 绝不能碰 | 聚合网关处理敏感文档、匿名免费 API 传敏感内容 | 接收方多达 34–61 家，不可控 |

## 2. 路径 A：公开创作内容 → 智谱 GLM（首选）

`glm-4.7-flash` / `glm-4.5-flash` **永久 $0 免费**，OpenAI 兼容，中文顶级，tool calling 成熟，**中国手机号注册，国内直连**，无需 VPN/信用卡。

```bash
# 1. 到 open.bigmodel.cn 注册，拿到 API key
# 2. 写入环境变量（建议放 ~/.zshrc）
export ZHIPU_API_KEY="你的key"
```

`~/.config/opencode/opencode.json`：

```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "zhipu": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Zhipu GLM",
      "options": { "baseURL": "https://open.bigmodel.cn/api/paas/v4" },
      "models": {
        "glm-4.7-flash": { "name": "GLM 4.7 Flash" },
        "glm-4.5-flash": { "name": "GLM 4.5 Flash" }
      }
    }
  }
}
```

坑点：高峰期可能排队；新用户另有 2000 万 tokens 体验额度（有效期未核实）；免费 tier 按官方政策可能用于服务改进——敏感文档仍走本地。

## 3. 路径 B：涉密文档 → 本地 Ollama（唯一安全答案）

权重下载到本机后推理**完全离线**，文档不经过任何网络。

```bash
# 1. 安装并拉权重（按 Mac 内存选）
brew install ollama
ollama pull qwen3:8b          # 16GB Mac
# ollama pull qwen3:30b-a3b   # 24GB+ Mac，本地 agentic 甜点区
```

`opencode.json` 加：

```json
{
  "provider": {
    "ollama-local": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Ollama（本机）",
      "options": { "baseURL": "http://localhost:11434/v1" },
      "models": {
        "qwen3:8b": { "name": "Qwen3 8B（本机）" },
        "qwen3:30b-a3b": { "name": "Qwen3 30B（本机）" }
      }
    }
  }
}
```

诚实提醒：本地模型工具选择失误率高于旗舰云端模型，复杂多步任务建议开 thinking 模式；Qwen 系中文顶级。

## 4. 路径 C：备选（按需）

| 方案 | 免费额度 | 门槛 | 说明 |
|---|---|---|---|
| Google AI Studio | Flash 约 10–15 RPM / 1500 RPD，无需卡 | 需 VPN；**免费 tier 数据可被 Google 用于训练** | agentic 强；敏感内容禁用 |
| Groq | 30 RPM / 1000 RPD / 200K TPD（按 org） | 邮箱注册，无需卡；大陆直连未核实 | 速度最快；200K/天只够轻量用 |
| OpenRouter `:free` | 20 RPM；< $10 消费仅 50 RPD | 需 VPN（未核实直连） | 50 RPD 对 agentic 不够用；多一跳经手 |
| Cloudflare Workers AI | 每天 10,000 neurons，无需卡 | Cloudflare 账号 | 低门槛里最值得试的 |
| 硅基流动 | 新用户 $1 credits | 中国手机号，国内直连 | 试用性质，用完即止 |

baseURL 速查：Groq `https://api.groq.com/openai/v1`，OpenRouter `https://openrouter.ai/api/v1`，Cloudflare（Workers AI OpenAI 兼容端点），key 一律走环境变量。

## 5. 聚合网关（技术实验用，不处理敏感文档）

- **free-claude-code**（`github.com/Alishahryar1/free-claude-code`，61k stars）：本地代理把 Claude Code/OpenCode 的请求转发到**自备 key** 的 49–61 家免费 tier；"13 亿 tokens/月"是各家免费 tier 加总的**理论值**，不是真送你 13 亿。Claude Code 指向第三方后端严格说可能违反其服务条款（未见执法）。
- **freellmapi**（`github.com/tashfeenahmed/freellmapi`，36.5k stars，MIT）：自托管 Node 网关，34 家/635 端点，key AES-256-GCM 本地加密，实现更干净。

两个都是"免费额度聚合器"，**数据经手方极多**，敏感文档禁用。

## 6. 强弱模型搭配（一句话路由）

> 错一次的代价 × 返工贵不贵 → 决定用强模型还是弱模型。
> 强模型（SOTA）：架构决策、复杂重构、深度长文终稿；
> 弱模型（Flash 级/GLM 免费）：草稿、批量脚本、格式转换、头脑风暴——配上你的验证回路，效果≈强模型，成本零头。

## 7. 未核实 / 待你在 Mac 上确认

- Mac 具体内存（决定 Ollama 跑 8B 还是 30B）
- Groq / OpenRouter 大陆直连情况
- 智谱 2000 万新用户额度有效期、豆包"协作奖励计划"口径

## 来源（2026-10-18 核验）

- opencode.ai/docs/zen（实测）｜ wallabytoken.com（2026-10-10）｜ qcode.cc（2026-10-15）
- Zhipu 官方定价页 ｜ Google AI Studio 限额文档 ｜ Groq 官方限额文档 ｜ OpenRouter 官方文档
- GitHub 官方公告（Models 2026-07-30 退役）｜ GitHub API（star 数实测）
- github.com/Alishahryar1/free-claude-code ｜ github.com/tashfeenahmed/freellmapi
