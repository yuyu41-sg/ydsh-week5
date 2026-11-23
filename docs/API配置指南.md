# API 配置指南（第 4 周）

> 密钥安全规范：所有敏感信息只存本地 `.env`（已被 .gitignore 排除，永不入库），
> 代码与 docker-compose.yml 均通过 `${VAR}` 环境变量引用，禁止硬编码。

## 一、.env 配置项说明

| 变量 | 用途 | 默认值 | 说明 |
|---|---|---|---|
| `ZHIPU_API_KEY` | 智谱大模型调用（NL2SQL/AI洞察） | 无（必填） | 格式 `32位.16位`，在 open.bigmodel.cn/usercenter/apikeys 创建 |
| `ZHIPU_BASE_URL` | 智谱 OpenAI 兼容端点 | https://open.bigmodel.cn/api/paas/v4/ | |
| `ZHIPU_MODEL` | 模型名 | glm-4-flash | 免费模型；如需更强推理可换 glm-4-plus |
| `MYSQL_ROOT_PASSWORD` | MySQL root 密码 | root | 元数据库 + 业务库共用 |
| `SUPERSET_SECRET_KEY` | Superset 会话加密 | ydsh-week4-secret | 生产环境必须换强随机值 |
| `SUPERSET_ADMIN_PASSWORD` | Superset admin 密码 | admin | 生产环境必须修改 |

## 二、密钥安全管理规范

1. **不入库**：`.env` 在 `.gitignore` 中；仓库只提交 `.env.example`（占位模板）
2. **不硬编码**：代码统一 `os.environ` / `load_dotenv` 读取；compose 用 `${VAR}` 注入容器环境变量
3. **权限最小化**：
   - Superset 数据库账号按库授权（本实训为 root 演示，生产应建只读账号给图表查询）
   - 大模型 Key 只在 app 服务容器内可见，Superset 容器不注入 LLM Key
4. **密钥轮换**：智谱控制台支持删除旧 Key 创建新 Key；轮换时只改 `.env` 后 `docker compose up -d app` 重启应用即可，无需改代码
5. **泄露应急**：Key 一旦出现在聊天记录/截图/日志中，立即在控制台删除并重建

## 三、大模型 API 最小化验证

```bash
python python/llm_client.py   # 或 week3 的脚本；期望输出：模型返回: ... token 用量: ...
```

## 四、Superset 数据源连接串（参考）

| 数据源 | SQLAlchemy URI |
|---|---|
| Hive | `hive://hive@ydsh-hiveserver2:10000/default`（容器网络内主机名） |
| MySQL | `mysql+pymysql://root:${MYSQL_ROOT_PASSWORD}@ydsh-mysql:3306/ydsh_ads` |

- 注意使用**容器网络内主机名**（ydsh-hiveserver2 / ydsh-mysql），不要写 localhost
- MySQL 走 pymysql 驱动；Superset 的 MySQL 类型映射需要 MySQLdb，
  本部署已在镜像内通过 sitecustomize.py 将 pymysql 伪装为 MySQLdb（见 部署手册.md）
- Hive 容器内需安装 `pyhive thrift thrift-sasl`（compose 首次启动命令已包含）

## 五、Streamlit 应用密钥注入

`docker-compose.yml` 的 app 服务：

```yaml
environment:
  ZHIPU_API_KEY: ${ZHIPU_API_KEY}   # .env 注入容器环境变量
```

应用代码经 `os.environ.get("ZHIPU_API_KEY")` 读取，`.env` 文件本身不进镜像、不进 Git。
