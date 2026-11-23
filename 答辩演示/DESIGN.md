# DESIGN.md · 云购生活数仓项目综合答辩

## 全局约定

- 画布 1280×720；内容页安全区：左右 40，页眉条 y0-56，内容区 y76-660，页脚 y664-700
- 页眉（A3 变体）：全宽 56px 主蓝 #1E4FA8 实色条，左侧白色粗体页标题 26px，右侧白色小字栏目归属
- 页脚：左"云购生活新零售数仓 · ydsh-team"14px 灰 #8B97A8，右页码 14px 深蓝
- 配色：主蓝 #1E4FA8 / 藏蓝 #0E3F8C / 浅蓝底 #E8EFF8、#F0F5FC / 中蓝 #3D7BD9 / 红 #D9534F / 黄 #FFC107 / 文 #1A2230、#4A5568、#8B97A8 / 线 #D6DCE5
- 字体：思源黑体系（Microsoft YaHei）；封面主标 54px，页标题 26px，卡内标题 20-22px，正文 15-17px，KPI 巨数字 64-84px，注释 13-14px
- 视觉母题：页眉蓝条 + 页码，全篇一致；卡片统一 #F7F9FC 底 + #D6DCE5 1px 描边，圆角 8
- 配图清单：
  | 文件 | 用途 | 来源 | 使用页 |
  |---|---|---|---|
  | assets/dashboard_top.png | 仪表板上半实拍（KPI/折线/品类/省份） | 用户真实截图 2502×1206 | P11 |
  | assets/dashboard_bottom.png | 仪表板下半实拍（漏斗/门店TopN） | 用户真实截图 2431×624 | P11 |
  | 其余页面用 SVG 结构图（架构图/流程/表格），无需生图 |

## 页面清单

| 页 | title | type | role/rhythm | layout | anti_pattern |
|---|---|---|---|---|---|
| 1 | 封面 | cover | hero/peak | 学术封面：主标+副标+汇报人 | 禁红金、禁人物照 |
| 2 | 目录 | catalog | supporting/valley | 左蓝栏+5条目 | 禁圆球编号 |
| 3 | 项目背景与建设目标 | content | supporting/valley | 三问题卡+目标条 | 禁空卡 |
| 4 | 总体架构：四层数仓 | content | supporting/valley | SVG 架构分层图+技术栈条 | 禁居中聚集 |
| 5 | 数据质量治理 | content | supporting/valley | 表格页（五类脏数据修复率）+结论条 | 禁表格小于70% |
| 6 | DWD 星型建模 | content | supporting/valley | 左事实/维度卡+右分区踩坑卡 | 禁等宽三卡 |
| 7 | 经营指标成果 | content | hero/peak | KPI 三联巨数字+洞察 | 禁数字与解读同行 |
| 8 | 销售预测与边界分析 | content | supporting/valley | 双栏对照（模型vs基线）+结论 | 禁50:50无结论 |
| 9 | NL2SQL 智能问数 | content | supporting/valley | 三道防线流程+测试结果条 | 禁纯文字罗列 |
| 10 | AI 洞察与人工验证 | content | supporting/valley | 幻觉案例对照卡+反思条 | 禁渲染警示色过量 |
| 11 | 可视化：仪表板与大屏 | content | hero/peak | 大图配文（两张实拍截图） | 禁图压字 |
| 12 | 一键部署与压测 | content | supporting/valley | 五服务编排SVG+压测数据 | 禁堆砌术语 |
| 13 | 文档与 Git 工程化 | content | supporting/valley | 左文档清单+右Git审查要点 | 禁罗列无结论 |
| 14 | 总结与展望 | ending | hero/peak | 中心总结+四要点+致谢 | 禁烟花装饰 |
