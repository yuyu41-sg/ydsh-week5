# Git 提交历史审查记录

项目：云购生活数仓（四周独立仓库）　　审查人：张宇　　日期：2026-11-23

## 一、仓库总览

| 仓库 | 分支 | 提交数 | 远端 | 内容 |
|---|---|---|---|---|
| ydsh-week1 | main | 15+ | github.com/yuyu41-sg/ydsh-week1 | 环境搭建、ODS、质量预评估、缺失值/去重清洗 |
| ydsh-week2 | main | 3 | github.com/yuyu41-sg/ydsh-week2 | 清洗进阶、DWD 建模、EDA、3 份 docx |
| ydsh-week3 | main + feature/nl2sql-tests + tag v0.1.0 | 9 | github.com/yuyu41-sg/ydsh-week3 | DWS/ADS、预测、LLM 接入、NL2SQL、AI 洞察 |
| ydsh-week4 | main | 2 | github.com/yuyu41-sg/ydsh-week4 | Superset、ECharts 大屏、Streamlit、Compose、压测 |

每周独立仓库的原因：实训按周评审提交，周与周交付物互不混淆（曾发生混周问题后拆分迁移，week1 中两次 chore 提交即为迁移留痕）。

## 二、约定式提交（Conventional Commits）核对

抽样全部历史提交 message，规范核对结果：

| 规范项 | 结果 |
|---|---|
| 类型前缀（feat/fix/docs/chore/merge） | ✅ 全部符合 |
| 描述用中文祈使句、一行说清 | ✅ |
| 正文详述改动点 | ✅ 关键提交均带多行 body |
| 敏感信息 | ✅ 无密钥入库（.env 全程被 .gitignore 排除，.env.example 提供模板） |

示例（week3）：
```
feat: NL2SQL 实测通过并新增报错自修复机制
- nl2sql.py 切换智谱 GLM 接入，实测 4 用例（3正例+1负例）全部通过
- 新增 repair_sql()：捕获 beeline 报错回传大模型自修复 SQL（最多2次重试）
```

## 三、分支结构与协同演练（week3 为例）

week3 完整演示了功能分支开发与 PR 协同：

```
*   afad759 Merge pull request #2 from yuyu41-sg/feature/nl2sql-tests
|\
| *   3b3c5b8 merge: 解决 README 冲突——保留 main 的自修复描述与 feature 的测试文档指引
| |\
|/|/
* | 1b51483 docs: README 补充 NL2SQL 自修复机制与实测结果（main 侧）
* | 3ec30e7 feat: 大模型接入切换为智谱GLM并完成AI洞察实测（main 侧）
| * 9546593 docs: README 关键成果补充实测通过率（feature 侧）
| * 5c18d4f feat: NL2SQL 实测通过并新增报错自修复机制
| * 27451e6 feat: 测试用例记录
|/
* 5f08a65 feat: 第3周基础交付
```

协同流程留痕（见 Git协同记录.md 与截图/）：
1. Issue #1：「NL2SQL 生成的 SQL 在 Hive 报 GROUP BY 别名错误（10004）」→ 与 PR 关联；
2. PR #2：feature/nl2sql-tests → main，制造真实 README 冲突（两分支各改同一行）；
3. GitHub 显示 "Can't automatically merge" → 本地融合式解决（两侧措辞都保留）→ PR 恢复可合并 → Merge → Issue #1 经 `Closes #1` 自动关闭；
4. Code Review：PR 页面行级评论留痕。

## 四、审查结论

1. 主干（main）历史清晰线性，无杂乱 merge 噪音；功能开发走 feature 分支并经 PR 合入；
2. 提交粒度与功能模块对应，每个子任务独立提交，可追溯；
3. 分支命名规范（feature/<模块>），合并后分支保留作为演练证据；
4. 无敏感信息泄露；未使用 force-push 破坏历史。

## 五、待改进

1. week4 提交粒度偏大（一次 25 文件），理想情况应按模块拆分（superset/大屏/app/compose 各一提）；
2. 各仓库可补充 CHANGELOG.md 自动生成流程（git log → 版本日志）。
