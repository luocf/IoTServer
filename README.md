# IoTServer
系统架构图
+------------+          +-------------+          +-------------+
| LoRaWAN    |  <-----> | LoRa Gateway|  <-----> | ChirpStack  |
| Devices    |          |             |          |             |
+------------+          +-------------+          +-------------+
                                                   |
                                                   |
                                    +--------------v--------------+
                                    |       FastAPI Backend        |
                                    |  - Device management &       |
                                    |    control                   |
                                    |  - Data processing & storage |
                                    |  - WebSocket for real-time   |
                                    |    communication             |
                                    +--------------+---------------+
                                                   |
                                                   |
                                         +---------v---------+
                                         |       Database     |
                                         +--------------------+
                                         |     Frontend (UI)   |
                                         +--------------------+

使用 FastAPI 和 ChirpStack 结合构建 IoT 系统，能够充分利用两者的优势，
创建一个高效、可扩展的设备管理与控制平台。FastAPI 提供了高性能的异步支持，适合处理实时通信和大量并发请求，
而 ChirpStack 则为 LoRaWAN 网络管理和设备数据处理提供了强大的功能。这一组合特别适合于需要实时监控和控制的物联网项目。

source myenv/bin/activate

使用 SQLAlchemy 和 Alembic 来构建 Python 侧的数据库和表

pip install sqlalchemy alembic

redis安装
使用Redis
启动 Redis 服务
使用系统服务管理工具启动 Redis（适用于系统服务配置的 Redis）：
在 Linux 上：
bash
sudo systemctl start redis
或
bash
sudo service redis-server start
在 macOS 上（如果通过 Homebrew 安装）：
brew install redis
bash
brew services start redis
直接运行 Redis 服务器（如果你没有将 Redis 配置为系统服务）：
在终端中执行：
bash
redis-server
验证 Redis 服务是否在运行
你可以使用 Redis CLI 工具来验证 Redis 服务是否正常运行：
bash
redis-cli ping
如果 Redis 正常运行，它会返回：
PONG
确保 Redis 服务启动后，你的 FastAPI 应用应该能够连接到 Redis 实例。如果你在本地运行 Redis，
确保它监听的是默认端口 6379，并且你的 FastAPI 应用配置了正确的 Redis 连接信息。

Alembic 数据库迁移
alembic init alembic
alembic revision --autogenerate -m "Updated models to match database design"
alembic upgrade head

uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload    

