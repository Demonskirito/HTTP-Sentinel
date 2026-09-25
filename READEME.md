# HTTP-Sentinel


基于 Vue 3、FastAPI 和 mitmproxy 的 Web 流量监控平台。😎😎

![](https://nianyun-art.oss-cn-hangzhou.aliyuncs.com/img/20260925143138091.png)

## 技术栈

- Frontend：Vue 3 + TypeScript + Vite
- Backend：FastAPI + Python 3.11
- Proxy：mitmproxy 9.0.1
- Deployment：Docker + Docker Compose

**1. 快速启动**

`1. 启动 Backend 和 Proxy`

在项目根目录执行：

`docker compose up -d --build`

查看运行状态：

`docker compose ps`

查看日志：

`docker compose logs -f`

**2. 启动前端**

进入前端目录：

`cd frontend`

安装依赖：

`npm install`

启动开发服务器：

`npm run dev`

默认访问：

`http://localhost:5173`

| 服务           | 地址                           |
| ------------ | ---------------------------- |
| Frontend     | `http://localhost:5173`      |
| Backend      | `http://localhost:8000`      |
| FastAPI Docs | `http://localhost:8000/docs` |
| Proxy        | `127.0.0.1:8080`             |
| Clash Verge  | `127.0.0.1:7897`             |

常用命令

启动：

`docker compose up -d --build`

停止：

`docker compose stop`

删除容器：

`docker compose down`

重新构建：

`docker compose up -d --build`

查看日志：

`docker compose logs -f`

Disclaimer

*本项目仅用于网络安全学习、研究及经过授权的安全测试环境。*