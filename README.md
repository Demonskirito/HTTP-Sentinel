# HTTP-Sentinel


基于 Vue 3、FastAPI 和 mitmproxy 的 Web 流量监控平台。😎😎

![](https://nianyun-art.oss-cn-hangzhou.aliyuncs.com/img/20260925143138091.png)

## 技术栈

- Frontend：Vue 3 + TypeScript + Vite
- Backend：FastAPI + Python 3.11
- Proxy：mitmproxy 9.0.1
- Deployment：Docker + Docker Compose

**快速启动**

**1. 启动 Backend 和 Proxy**

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


🔐 HTTPS 监测配置

本项目通过 mitmproxy 代理 HTTPS 流量，因此首次使用需要安装项目生成的 mitmproxy CA 证书。

⚠️ 安全提示

mitmproxy CA 是一个根证书。安装后，当前系统会信任由该 CA 签发的代理证书。
建议仅在自己的电脑、实验环境或经过授权的测试环境中使用。

不要将 mitmproxy-ca.pem、私钥等敏感文件提交到 GitHub。

**获取 CA 证书**

启动 mitmproxy 后，让浏览器代理到：

`127.0.0.1:8080`

然后浏览器访问：

`http://mitm.it`

会出现 mitmproxy 的证书安装页面。

选择：Windows

下载/安装对应的 CA 证书。

CMD 安装 mitmproxy CA

假设证书就在项目根目录：

`certutil -addstore -user Root mitmproxy-ca-cert.cer`

成功后一般会看到类似：

`Root "受信任的根证书颁发机构"
CertUtil: -addstore 命令成功。`


CMD 验证证书

可以执行：

`certutil -user -store Root`

然后搜索：

`mitmproxy`

如果看到：

`Subject: CN=mitmproxy
Issuer: CN=mitmproxy`

说明 CA 已经安装。

说明 CA 已经安装到当前用户的受信任根证书存储区。

Disclaimer

*本项目仅用于网络安全学习、研究及经过授权的安全测试环境。*
