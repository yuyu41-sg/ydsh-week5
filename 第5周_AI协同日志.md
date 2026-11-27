# 第 5 周 AI 协同日志

- 团队：ydsh-team　成员：张宇（20230308059）　填写日期：2026-11-27（综合覆盖第 4~5 周）

---

## 一、使用的 AI 工具 / 模型

- 工具名称：WorkBuddy 内置大模型　模型版本：WorkBuddy Agent（系统排障 + 脚本生成 + 方案验证 + 文档与答辩材料生成）
- 辅助环境：Docker Compose（MySQL 8.0 / Hive 4.0 / Superset 6.0 / Streamlit）、Git、GitHub

---

## 二、AI 协同记录表（至少 5 条）

| 序号 | 提问 / 任务描述 | AI 产出摘要 | 人工修改与验证 | 是否采纳 |
|------|----------------|-------------|----------------|----------|
| 1 | 排查 ECharts 经营大屏打开后图表全部空白 | 定位为 CDN 静态资源被墙导致 echarts.min.js / china.js 加载失败，给出改用国内镜像下载并本地引用的方案 | 人工从 npmmirror 下载两份 JS 放入 bigscreen 目录并改 index.html 为本地引用，断网实测大屏完整渲染 | 是 |
| 2 | 重建环境后重放第 1 周数据脚本，GMV 与交付文档对不上（差异约 1.9 万） | AI 先按"重放漂移"思路协助定位容器挂载路径问题（/sql 指错目录、data/ 缺 CSV、dim/ 缺维表），修复后仍差 1.9 万；随后人工与 AI 联合复盘，AI 编写比对脚本证明 dwd_order 去重用了 ROW_NUMBER 窗口函数，198 组并列冲突行保留哪一行是随机的，重放**原理上不可复现** | 人工决定放弃重放，改为"保留 ODS 原始数据文件 + 重建 10 张外部表 DDL + MSCK 修复分区"方案，AI 生成 restore_meta.sql，恢复后 KPI（GMV 14,151,214.68 / 订单 5642 / 客单价 2508.19）与交付文档分毫不差 | 是（换了方案） |
| 3 | 容器删除后 Hive 元数据丢失（metastore 用容器内 Derby） | AI 解释 Derby 数据随容器层销毁而丢失，并给出外部表挂载 + beeline -f 执行恢复脚本 | 人工实测 beeline -f 遇错即停导致恢复中断，改用容器内 pyhive 直连逐条执行，10 张表全部注册成功 | 是（修正执行方式） |
| 4 | 修复 Streamlit 智能问答容器内报错 | ① 脚本调用宿主机 docker 命令但容器内无 docker CLI——AI 给出 pyhive 直连 HiveServer2 替代方案（PLAIN 认证只需 thrift-sasl 不需 sasl，从 Dockerfile 移除避免编译失败）；② app.py 报错 err 未定义——人工补成功标志位 | 两处修复后问答链路实测跑通，"月度趋势"用例修正为直接使用 order_month 分区列 | 是 |
| 5 | 排查 Superset 连接 Hive 失败（422） | AI 定位为 MySQL 驱动安装位置错误：docker compose 启动命令用了 pip --system，而 Superset 6 实际运行在 /app/.venv 虚拟环境 | 人工改用 uv pip install --python /app/.venv/bin/python 并配 sitecustomize.py 注入 pymysql.install_as_MySQLdb()，实测连接恢复 | 是 |
| 6 | 重建 Superset 仪表板（旧卷布局数据损坏，PUT 接口 500） | AI 摸清 position_json 必须 ROOT→TABS→GRID 三层嵌套、ROW 的 children 必须是字符串 ID 而非 dict 对象（否则接口永久 500）；编写 superset_charts.py 用 REST API 重建 | 人工实跑发现图表仍显示 "no chart definition"——AI 进一步定位 API 不会从 position_json 自动同步 slices 关系，补一段 docker exec 内 ORM 挂载（dash.slices = query(Slice).filter(id.in_(...))），6 个图表全部恢复渲染 | 是 |
| 7 | 编写 NL2SQL few-shot 提示词的月度趋势示例 | 生成基于 SUBSTR 截取月份 + 别名分组的示例 | 人工指出 Hive 禁止别名分组（第 3 周已踩过同类坑），改为直接使用 order_month 分区列的写法，并在系统提示词中强化规则 8 | 是（修正了写法） |
| 8 | 答辩材料整理：逐页讲稿、高频追问预案、PPT 截图页、Git 历史审查记录、英文 README | AI 生成答辩讲稿初稿（14 页 9 分钟话术 + 时间锚点 + 必背数字）、Git 历史审查记录与英文 README 初稿 | 人工逐页核对必背数字与数仓实查一致（GMV 1415.12 万 / 订单 5642 / 客单价 2508.19 / 复购用户 997 / 复购率 98.09%），替换 PPT 截图为真实运行截图（v2），补充三入口演示动线并做环境全绿验证 | 是 |

---

## 三、AI 产出成果清单

- 由 AI 生成的内容（代码 / SQL / 文案 / 图表）：restore_meta.sql（10 张外部表 DDL + MSCK）；dedup_diff.py / rule_search.py（冲突行比对验证）；superset_charts.py（REST API 重建仪表板 + ORM 补挂）；Dockerfile 与 docker-compose.yml 修复片段；答辩讲稿、Git 历史审查记录、英文 README、答辩 PPT 截图页
- 由人工编写的内容：数据一致性危机的最终方案决策（放弃重放改外部表挂载）、KPI 逐项核对、冲突行"无规律可循"的结论判读、pyhive 直连替代 docker exec 的执行方式修正、few-shot 月度示例的方言修正、答辩演示动线设计
- 人机协作完成的内容：大屏与三入口环境恢复全链路（AI 排障 + 人工实跑验证）；Superset 6 恢复链路踩坑知识固化进脚本实现一键复现；答辩三件套（准备清单 / 讲稿 / PPT）的生成与人工审校

---

## 四、问题与解决

- 遇到的问题：① 重放数据 GMV 漂移 1.9 万且无法收敛；② Derby 元数据随容器删除丢失；③ Superset 驱动装错环境导致 422；④ 坏布局导致仪表板接口永久 500 且先解析旧值即死锁；⑤ CDN 被墙大屏空白；⑥ 容器内无 docker CLI
- AI 是否有效解决：全部有效解决（8/8，其中 2 项 AI 首个方案被人工修正后收敛：分区重放→外部表挂载、别名分组→分区列直用）
- 最终如何解决：① 证明不可复现后改挂载原始文件 + 重建元数据，KPI 与文档完全一致；② 外部表 + MSCK 重建注册；③ 驱动改装 /app/.venv + sitecustomize；④ 删除坏仪表板经 API 重建 + ORM 补挂 slices；⑤ 静态资源本地化；⑥ pyhive 直连 HiveServer2

---

## 五、反思与总结

- AI 协同带来的价值：两周内完成了一场"小型生产事故"的完整处置——从数据漂移定位、元数据灾难恢复到环境一键复现，AI 把各组件（Hive/Superset/Streamlit/Docker）的排查时间从数小时压缩到分钟级；所有踩坑经验固化进脚本后，环境重建从半天变成一键
- AI 的局限与风险（准确性 / 合规性 / 依赖）：AI 倾向给出"表面合理"的第一方案（重放、别名分组），但对数据随机性、方言约束这类需要看真实数据的约束缺乏先验，必须人工实跑验证；不加拦截的自动化操作（直接 PUT 坏布局）可能造成死锁式损坏；对工具链内部机制（.venv、ORM 关系不随 JSON 同步）的假设需逐一验证
- 本次协作中我的能力提升：建立了"先证伪、再换路"的排障方法论——用比对脚本证明重放原理上不可复现，比反复重试更省时间；学会把恢复过程沉淀为可复现脚本而非一次性手工操作；答辩数字全部以实查回溯为准，杜绝引用幻觉数字
- 对 AI 协同的改进建议：涉及不可复现操作（重放、覆盖写入）前，先让 AI 输出"可复现性评估"再动手；基础设施类修复应强制要求附带验证命令（curl 实查、KPI 比对）；把团队两周的踩坑记录沉淀为共享的排障知识库，供后续项目复用
