# Docker 相关说明

## 当前状态

项目已重新支持 **Dockerfile / docker-compose** 部署方案。该方案主要针对 **后端 API** 的容器化，方便在 Linux 服务器或 NAS 环境下长期稳定运行。

## 快速开始

如果你已安装 Docker 和 Docker Compose，可以通过以下步骤启动后端：

### 1. 配置环境

在项目根目录创建 `.env` 文件（如果没有的话），并填入必要的 API 密钥（如 DeepSeek）：

```env
LLM_PROVIDER=deepseek
DEEPSEEK_API_KEY=sk-your-api-key
DEEPSEEK_MODEL=deepseek-reasoner
LOG_LEVEL=INFO
```

### 2. 启动服务

使用 Docker Compose 启动：

```bash
# 启动服务
docker-compose up -d
```

或者使用 Makefile 中预置的任务：

```bash
# 构建镜像
make docker-build

# 启动服务 (生产模式)
make docker-up
```

### 3. 验证

启动后，API 默认监听在 `8000` 端口。你可以通过以下地址验证：

- 健康检查: `http://localhost:8000/health`
- API 文档: `http://localhost:8000/docs`

## SQLite 数据持久化

Docker 配置中已预设了两个本地目录挂载：

- `./data` -> `/app/data`: 存放 SQLite 数据库文件 (`secbot.db`)
- `./logs` -> `/app/logs`: 存放运行日志

这意味着即使容器被删除，你的扫描历史和配置数据也会保留在宿主机的 `data` 目录中。

## 局限性与说明

1. **Terminal UI (TUI)**: TUI 依赖真实的 TTY 和交互式输入，不适合在 Docker 容器内作为常驻服务运行。建议将容器作为后端，在宿主机或其它机器上通过 `python main.py` 连接该后端的 API 地址。
2. **端口冲突**: 如果宿主机的 `8000` 端口已被占用，请修改 `docker-compose.yml` 中的 `ports` 映射。

## 常用命令

- 查看日志: `docker-compose logs -f`
- 停止服务: `docker-compose down`
- 重新构建镜像: `docker-compose build --no-cache`
