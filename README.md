# XingTu Harness · 一线 AI 工程化脚手架

> **一个仓库，一键拿到全部行途开源资产。** 聚合自有 + 市面优秀开源，按领域场景开箱即用。

![License](https://img.shields.io/badge/license-MIT-green.svg)
![Submodules](https://img.shields.io/badge/submodules-8-blue.svg)
![Scenarios](https://img.shields.io/badge/scenarios-7-purple.svg)
![Git Submodule](https://img.shields.io/badge/vcs-git%20submodule-orange.svg)

---

## 🎯 这是什么

`xingtu-harness` 是行途开源矩阵的**中央聚合仓**。它不是又一个工具，而是把散落在独立仓库里的 AI 工程资产（skills / hooks / rules / specs / MCP / CLI / 工具）通过 **git submodule** 聚合到一起，并按**领域场景**提供开箱即用的脚手架。

**给谁用**：技术管理者、一线工程师、AI 工程化实践者——想快速搭起一套可用的 Agent/Skill 工作台，不用从零踩坑。

## 🧩 与 DeepSeek Harness（DSH）的关系

本仓与 DeepSeek Harness（DSH，「一切皆插件」的 Agent 运行时）互为补充：DSH 提供可插拔的运行时底座，本仓提供经过生产验证的 **skills / hooks / rules / specs / MCP / CLI** 资产，可直接在 DSH 之上组装使用。各子仓均标注 DSH 兼容格式。

## 🚀 快速开始

### 方式一：一键拉全（推荐）

```bash
git clone --recurse-submodules https://github.com/xingtu1996/xingtu-harness.git
cd xingtu-harness
./install.sh
```

### 方式二：按场景安装

```bash
# 查看可用场景
./harness list

# 只装某个场景（例：微服务项目）
./harness install scene:microservice
```

## 🧩 场景矩阵（按领域开箱即用）

| 场景 | 说明 | 覆盖资产 |
|------|------|---------|
| `presale` | 售前支持 | specs / skills |
| `admin` | 行政事务 | rules / skills |
| `coding-0to1` | 新项目从零搭建 | skills / hooks / specs |
| `coding-1ton` | 存量项目迭代 | skills / hooks / rules |
| `monolith` | 单体项目 | skills / cli |
| `microservice` | 微服务项目 | skills / rules / mcp |
| `finance` | 财务场景 | rules / specs |

> 场景清单持续扩展中，欢迎提 PR 补充。

## 📦 聚合的子模块

本仓通过 git submodule 引用以下 **8 个**独立仓库（各自可独立分发、独立收藏）：

| 子模块 | 说明 |
|--------|------|
| [xingtu-skills](https://github.com/xingtu1996/xingtu-skills) | AI Agent 技能库 |
| [xingtu-hooks](https://github.com/xingtu1996/xingtu-hooks) | Claude Code 钩子 |
| [xingtu-rules](https://github.com/xingtu1996/xingtu-rules) | 规则工程化 |
| [xingtu-sdd](https://github.com/xingtu1996/xingtu-sdd) | SDD 规格方法论 |
| [xingtu-mcps](https://github.com/xingtu1996/xingtu-mcps) | MCP 服务 |
| [xingtu-cli](https://github.com/xingtu1996/xingtu-cli) | 命令行工具 |
| [xingtu-tools](https://github.com/xingtu1996/xingtu-tools) | 工程脚本 |
| [tokenhub-bench](https://github.com/xingtu1996/tokenhub-bench) | 模型评测 |

> ⭐ **关联旗舰仓（独立仓库，非 submodule）**：[xingtu-ai-engineering](https://github.com/xingtu1996/xingtu-ai-engineering) — 方法论旗舰仓：理念/方法/五大工程/治理/会话/样板

## 🤖 AI 可检索

`marketplace.json` 提供机器可读的资产索引，供 find-skills / AI 搜索引擎检索：

```bash
# 查看完整索引
cat marketplace.json
```

## 📄 许可证

MIT License。所有聚合资产版权归各自仓库作者，引用时请保留上游 LICENSE。
