# XSA 仓库治理与工程规范（草案）

借鉴 DeepSeek Harness 的模块化、AGENTS、CONTRIBUTING、安全规范和测试基建，但第一阶段不照搬其大规模 monorepo。

## 必备文件

README.md（中文主入口）、README.en.md、LICENSE、AGENTS.md、CONTRIBUTING.md、CODE_OF_CONDUCT.md、SECURITY.md、CHANGELOG.md、docs/ARCHITECTURE.md、docs/PHILOSOPHY.md、docs/ROADMAP.md、docs/REFERENCES.md、tests/、examples/、templates/、.github/PULL_REQUEST_TEMPLATE.md、.github/workflows/ci.yml。

## PR 纪律

1. Issue / SDD → 隔离分支 → 测试 → Draft PR → 独立审核 → 人工合并。
2. 所有新适配器声明 capability、transport、权限、验证时间与失败回退。
3. 统一状态：design / mock / verified / production。README 不展示尚未验证能力为“已支持”。
4. 不修改外部仓库的生产任务；跨仓兼容升级按仓分别 PR。
5. 任何公开演示不得包含个人路径、原始对话、访问令牌、内部项目和私有 GitHub 内容。
6. 先稳定协议，再加入复杂编排；每项架构调整出 ADR，拒绝无证据的“性能更好”宣传。

## CI 最小门禁

- 语法检查、单元测试、Schema 校验、Secret 扫描；
- 重复事件幂等与未经授权阻断测试；
- 文档链接与示例可运行检查；
- 不在外部 PR 默认授予写权限，不运行不可信贡献者代码访问 secrets。

## 里程碑

v0.1 离线协议与模拟器 → v0.2 持久化/恢复/只读 GitHub Adapter → v0.3 授权真实 Worker 接力 → v1.0 第三方可安装模板与稳定接口。版本号仅表示计划，不表示已发布。

## 跨仓战略

XSA 负责协议、能力目录和集成路线；xingtu-harness/skills/hooks/cli/scheduled/learn/vault 等仓保持独立。成熟技术按 PR 双向回流；公开产品不依赖私有 vault。

## 评估

A/B 观察人工交接次数、总耗时、按实测 Token/费用、质量评分、重复副作用、恢复时间。目标“人工交接下降70%”“高能力调用下降30%”为研究假设，不能描述为实绩。
