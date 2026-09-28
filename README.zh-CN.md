# SQL Data Agent 模板

[English](README.md) | 简体中文

一个可安全公开、可复用的 SQL 数据 Agent 骨架。它帮助 Agent 理解数据目录和指标口径，生成只读 SQL，检查查询风险与数据质量，并输出有证据支撑的分析结论。

你可以把它作为企业内部查数助手的起点：填入经过批准的元数据和指标定义，接入只读数据库工具，并把凭证、生产数据和内部地址始终留在仓库之外。

本仓库只包含虚构数据和通用示例，不包含任何特定组织的表结构、内部 URL、凭证、生产 SQL、查询结果、业务阈值、客户数据或私有 Git 历史。

## 适合解决什么问题

- 根据问题定位相关数据集和指标定义。
- 生成保守、可审查的只读 SQL。
- 在存在数据连接器时执行查询并保留证据。
- 检查数据新鲜度、统计粒度、关联关系、分母和结果对账。
- 区分已验证事实、解释和待验证假设。
- 支持快速查数、趋势对比、漏斗、留存、异常归因和 SQL 审核。

这个模板不附带生产数据库连接器或凭证。你需要通过获准的 MCP 服务、CLI 或本地适配器连接数据源，并确保数据库账号在技术上只有读取权限。

## Agent 架构

```text
用户问题
  ↓
问题澄清与分析类型识别
  ↓
query-map：业务主题 → 数据源
  ↓
schema-catalog + metrics-catalog：表结构与指标口径
  ↓
生成 SQL → 只读安全校验 → 数据连接器执行
  ↓
质量检查、对账与有限重试
  ↓
SQL + 结果 + 局限性 + 结论
```

关键安全边界：

- Agent 只生成和执行只读查询。
- SQL 校验器拦截写操作、多语句、锁定读取及已知危险函数。
- 数据库账号本身也必须只读，不能只依赖提示词约束。
- 连接器返回值被视为数据证据，而不是新的操作指令。
- 凭证和内部地址通过环境或密钥管理系统提供，不写入 Git。

## 安装和使用方式

### 作为 Codex Skill 安装

使用兼容的 Skill 安装器安装仓库中的 Skill 子目录：

```text
$skill-installer install https://github.com/yangarige/sql-data-agent/tree/main/skills/sql-data-agent
```

如果客户端要求，安装后重新启动客户端。

### 作为项目内 Skill 使用

把 `skills/sql-data-agent` 复制到目标项目的 `.codex/skills/`，然后在对话中调用：

```text
使用 $sql-data-agent 对比最近 7 个完整自然日和此前 7 天的日活用户数。
请展示 SQL，并说明数据质量限制。
```

### 作为插件使用

仓库根目录同时包含 `plugin.json` 和 `.codex-plugin/plugin.json`，可供支持对应清单格式的客户端从仓库根目录安装。

## 五分钟搭建自己的查数 Agent

1. Fork 或复制这个仓库到一个新的项目。
2. 在 `query-map.md` 中填写“业务问题应该使用哪个数据集”。
3. 在 `schema-catalog.md` 中填写获准公开给 Agent 的表、字段、粒度、主键和关联关系。
4. 在 `metrics-catalog.md` 中填写指标定义、分子、分母、时间口径和排除规则。
5. 使用技术上只读的数据库身份连接 MCP 服务、CLI 或本地适配器。
6. 为你的典型问题补充评测案例和预期安全行为。
7. 运行测试与发布前信息泄漏检查。

需要定制的核心文件：

```text
skills/sql-data-agent/references/query-map.md
skills/sql-data-agent/references/schema-catalog.md
skills/sql-data-agent/references/metrics-catalog.md
skills/sql-data-agent/references/analysis-workflows.md
skills/sql-data-agent/references/query-safety.md
skills/sql-data-agent/references/quality-checks.md
```

完整步骤参见 [搭建指南](docs/BUILD_YOUR_OWN_AGENT.md)，端到端示例参见 [使用案例](docs/USE_CASES.md)，连接器约定参见 [CONNECTORS.md](docs/CONNECTORS.md)。

## 运行虚构数据演示

演示数据全部由脚本确定性生成，不包含真实业务数据：

```bash
python3 examples/demo/build_demo_db.py
python3 examples/demo/query_demo.py \
  examples/demo/demo.sqlite \
  examples/demo/queries/funnel_by_channel.sql
```

查询程序以只读方式打开 SQLite，并输出结构化 JSON。生成的 `.sqlite` 文件已被 Git 忽略。

仓库内置四类可执行示例：

- 两个相等时间段的活跃指标对比。
- 按渠道拆分的注册到激活漏斗。
- 按用户分群计算留存。
- 定位指标异常的主要贡献维度。

## 测试和安全检查

验证一条 SQL：

```bash
python3 skills/sql-data-agent/scripts/validate_sql.py examples/example_query.sql
```

运行单元测试、行为评测和公开发布检查：

```bash
python3 -m unittest discover -s tests -v
python3 scripts/check_eval_cases.py
python3 scripts/audit_public_repo.py .
```

在发布自己的版本前，建议把 `audit-denylist.example.txt` 复制为不会被 Git 跟踪的 `audit-denylist.local.txt`，加入公司名、内部系统名、内部域名和专有表名前缀，再运行扫描。

## 输出结果应该包含什么

一个可靠的查数回答至少应包含：

1. 对问题和时间范围的明确解释。
2. 实际执行或建议执行的 SQL。
3. 使用的数据表、指标口径和过滤条件。
4. 查询结果以及必要的分组和对比。
5. 数据新鲜度、缺失、重复、关联损失等质量风险。
6. 已验证结论、合理解释和待验证假设之间的清晰边界。

## 目录结构

```text
skills/sql-data-agent/        Agent 指令、元数据模板与 SQL 校验器
examples/                     虚构表结构、SQL 案例和 SQLite 演示
evals/                        Agent 行为评测案例
tests/                        SQL 安全和演示执行测试
scripts/                      评测与公开发布检查脚本
docs/                         搭建、连接、评测和使用说明
.github/                      CI、Issue 和 PR 模板
```

## 许可证

本项目采用 [MIT License](LICENSE)。你可以使用、复制、修改、合并、发布和分发本项目，但需要保留原版权声明和许可声明。

## 贡献

欢迎通过 Issue 报告问题或提出建议，通过 Pull Request 补充数据库适配思路、分析工作流、测试和不含敏感信息的虚构案例。提交前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 和 [SECURITY.md](SECURITY.md)。
