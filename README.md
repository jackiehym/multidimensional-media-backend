# 后端开发文档

## 一、文档基本信息

### 1. 项目名称
Multidimensional Media Backend

### 2. 项目目标与功能概述
本项目是一个多维媒体管理系统的后端服务，旨在为前端应用提供数据持久化存储和API接口。核心功能包括：

- **媒体文件管理**：添加、批量添加、删除、更新媒体文件
- **标签系统**：管理媒体文件的标签，支持添加、删除、重命名、合并标签
- **标签分类**：管理标签的分类，支持添加、删除、修改分类
- **文件名解析**：从文件名自动提取标签、年份等信息
- **文件存储**：支持媒体文件的上传、存储和访问

### 3. 技术栈说明
- **后端框架**：FastAPI 0.100+
- **数据库**：SQLite 3.36+
- **ORM**：SQLAlchemy 2.0+
- **数据验证**：Pydantic 2.0+
- **文件存储**：本地文件系统
- **API规范**：RESTful

## 二、环境配置与依赖

### 1. 开发环境要求
- Python 3.9+
- 操作系统：Windows、Linux、macOS
- 虚拟环境工具：Conda 或 venv

### 2. 依赖安装说明

使用 Conda 创建虚拟环境：
```bash
conda create -n media-backend python=3.9
conda activate media-backend
pip install -r requirements.txt
```

使用 venv 创建虚拟环境：
```bash
python -m venv venv
# Windows
env\Scripts\activate
# Linux/macOS
source venv/bin/activate
pip install -r requirements.txt
```

### 3. 环境变量配置

创建 `.env` 文件，配置以下环境变量：

| 变量名 | 描述 | 示例值 |
|--------|------|--------|
| DATABASE_URL | 数据库连接字符串 | sqlite:///./media.db |
| MEDIA_DIR | 媒体文件存储目录 | ./media |
| UPLOAD_DIR | 临时上传目录 | ./uploads |
| PORT | 服务端口 | 8000 |
| HOST | 服务主机 | 0.0.0.0 |
| ENVIRONMENT | 运行环境 | development |

### 4. 启动命令

**开发环境**：
```bash
# Windows
run.bat

# 或直接运行
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

**生产环境**：
```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

## 三、API 设计与规范

### 1. API 根路径
`http://localhost:8000/api`

### 2. 认证与授权机制
本项目为个人本地使用，不需要用户认证和授权机制。

### 3. 端点列表

#### 3.1 媒体文件相关 API

| 方法 | 路径 | 功能描述 | 请求体 (JSON) | 成功响应 (200 OK) |
|------|------|----------|--------------|------------------|
| GET | /api/media | 获取媒体文件列表 | N/A | `[{"id": 1, "filename": "...", "path": "...", "tags": [...], ...}]` |
| GET | /api/media/{id} | 获取单个媒体文件 | N/A | `{"id": 1, "filename": "...", "path": "...", "tags": [...], ...}` |
| POST | /api/media | 添加媒体文件 | `{"filename": "...", "path": "...", "tags": [...], ...}` | `{"id": 1, "filename": "...", "path": "...", "tags": [...], ...}` |
| POST | /api/media/bulk | 批量添加媒体文件 | `{"items": [{"filename": "...", "path": "...", "tags": [...], ...}]}` | `{"success": true, "count": 5}` |
| PUT | /api/media/{id} | 更新媒体文件 | `{"filename": "...", "tags": [...], ...}` | `{"id": 1, "filename": "...", "path": "...", "tags": [...], ...}` |
| DELETE | /api/media/{id} | 删除媒体文件 | N/A | `{"success": true}` |
| DELETE | /api/media/bulk | 批量删除媒体文件 | `{"ids": [1, 2, 3]}` | `{"success": true, "count": 3}` |
| POST | /api/media/upload | 上传文件 | `file: <文件>` | `{"path": "...", "filename": "...", "size": 1024}` |
| POST | /api/media/add-tag | 为媒体文件添加标签 | `{"media_ids": [1, 2, 3], "tag_name": "...", "category": "..."}` | `{"success": true}` |
| POST | /api/media/remove-tag | 从媒体文件移除标签 | `{"media_ids": [1, 2, 3], "tag_name": "..."}` | `{"success": true}` |

#### 3.2 标签相关 API

| 方法 | 路径 | 功能描述 | 请求体 (JSON) | 成功响应 (200 OK) |
|------|------|----------|--------------|------------------|
| GET | /api/tags | 获取标签列表 | N/A | `[{"id": 1, "name": "...", "category": "...", "color": "..."}]` |
| POST | /api/tags | 添加标签 | `{"name": "...", "category": "...", "color": "..."}` | `{"id": 1, "name": "...", "category": "...", "color": "..."}` |
| PUT | /api/tags/{id} | 更新标签 | `{"name": "...", "category": "...", "color": "..."}` | `{"id": 1, "name": "...", "category": "...", "color": "..."}` |
| DELETE | /api/tags/{id} | 删除标签 | N/A | `{"success": true}` |
| POST | /api/tags/rename | 重命名标签 | `{"old_name": "...", "new_name": "..."}` | `{"success": true}` |
| POST | /api/tags/merge | 合并标签 | `{"source_names": ["..."], "target_name": "..."}` | `{"success": true}` |
| POST | /api/tags/bulk-delete | 批量删除标签 | `{"names": ["..."]}` | `{"success": true, "count": 2}` |
| POST | /api/tags/change-category | 更改标签分类 | `{"tag_name": "...", "new_category": "..."}` | `{"success": true}` |

#### 3.3 标签分类相关 API

| 方法 | 路径 | 功能描述 | 请求体 (JSON) | 成功响应 (200 OK) |
|------|------|----------|--------------|------------------|
| GET | /api/categories | 获取分类列表 | N/A | `[{"id": 1, "key": "...", "label": "...", "emoji": "...", "color": "...", "built_in": false}]` |
| POST | /api/categories | 添加分类 | `{"key": "...", "label": "...", "emoji": "...", "color": "..."}` | `{"id": 1, "key": "...", "label": "...", "emoji": "...", "color": "...", "built_in": false}` |
| PUT | /api/categories/{id} | 更新分类 | `{"label": "...", "emoji": "...", "color": "..."}` | `{"id": 1, "key": "...", "label": "...", "emoji": "...", "color": "...", "built_in": false}` |
| DELETE | /api/categories/{id} | 删除分类 | N/A | `{"success": true}` |
| POST | /api/categories/seed | 初始化默认数据 | N/A | `{"success": true, "message": "Default data seeded successfully"}` |

#### 3.4 其他 API

| 方法 | 路径 | 功能描述 | 响应 |
|------|------|----------|------|
| GET | / | 欢迎信息 | `{"message": "Welcome to Media Management API"}` |
| GET | /health | 健康检查 | `{"status": "healthy"}` |

### 4. 示例请求与响应

#### 示例 1: 添加媒体文件

**请求**：
```bash
curl -X POST "http://localhost:8000/api/media" \
  -H "Content-Type: application/json" \
  -d '{"filename": "example.mp4", "path": "/media/example.mp4", "tags": ["action", "2023"], "year": 2023, "resolution": "1080p"}'
```

**响应**：
```json
{
  "id": 1,
  "filename": "example.mp4",
  "path": "/media/example.mp4",
  "tags": ["action", "2023"],
  "year": 2023,
  "resolution": "1080p",
  "added_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

#### 示例 2: 获取标签列表

**请求**：
```bash
curl "http://localhost:8000/api/tags"
```

**响应**：
```json
[
  {"id": 1, "name": "action", "category": "genre", "color": "270 60% 55%"},
  {"id": 2, "name": "2023", "category": "year", "color": "120 60% 55%"}
]
```

## 四、数据库设计与模型

### 1. 数据模型

**媒体文件表 (media_items)**
| 字段名 | 数据类型 | 约束 | 描述 |
|-------|---------|------|------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT | 媒体ID |
| filename | VARCHAR(255) | NOT NULL | 文件名 |
| path | VARCHAR(512) | NOT NULL | 文件路径 |
| year | INTEGER | NULL | 年份 |
| resolution | VARCHAR(50) | NULL | 分辨率 |
| rating | INTEGER | NULL | 评分 |
| added_at | TIMESTAMP | NOT NULL DEFAULT CURRENT_TIMESTAMP | 添加时间 |
| updated_at | TIMESTAMP | NOT NULL DEFAULT CURRENT_TIMESTAMP | 更新时间 |

**标签表 (tags)**
| 字段名 | 数据类型 | 约束 | 描述 |
|-------|---------|------|------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT | 标签ID |
| name | VARCHAR(100) | NOT NULL UNIQUE | 标签名称 |
| category | VARCHAR(50) | NOT NULL | 标签分类 |
| color | VARCHAR(50) | NOT NULL | 标签颜色 |
| created_at | TIMESTAMP | NOT NULL DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | NOT NULL DEFAULT CURRENT_TIMESTAMP | 更新时间 |

**标签分类表 (tag_categories)**
| 字段名 | 数据类型 | 约束 | 描述 |
|-------|---------|------|------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT | 分类ID |
| key | VARCHAR(50) | NOT NULL UNIQUE | 分类键 |
| label | VARCHAR(100) | NOT NULL | 分类标签 |
| emoji | VARCHAR(10) | NOT NULL | 分类 emoji |
| color | VARCHAR(50) | NOT NULL | 分类颜色 |
| built_in | BOOLEAN | NOT NULL DEFAULT false | 是否内置 |
| created_at | TIMESTAMP | NOT NULL DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | NOT NULL DEFAULT CURRENT_TIMESTAMP | 更新时间 |

**媒体标签关联表 (media_tags)**
| 字段名 | 数据类型 | 约束 | 描述 |
|-------|---------|------|------|
| media_id | INTEGER | REFERENCES media_items(id) | 媒体ID |
| tag_id | INTEGER | REFERENCES tags(id) | 标签ID |
| PRIMARY KEY | (media_id, tag_id) | | 复合主键 |

### 2. SQLAlchemy 模型

**媒体文件模型** (`app/models/media.py`):
```python
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table, func
from sqlalchemy.orm import relationship

from app.db.base import Base


media_tags = Table(
    "media_tags",
    Base.metadata,
    Column("media_id", Integer, ForeignKey("media_items.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True)
)


class MediaItem(Base):
    __tablename__ = "media_items"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    filename = Column(String(255), nullable=False)
    path = Column(String(512), nullable=False)
    year = Column(Integer, nullable=True)
    resolution = Column(String(50), nullable=True)
    rating = Column(Integer, nullable=True)
    added_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    tags = relationship("Tag", secondary=media_tags, back_populates="media_items")
```

**标签模型** (`app/models/tag.py`):
```python
from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.media import media_tags


class Tag(Base):
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    category = Column(String(50), nullable=False)
    color = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    media_items = relationship("MediaItem", secondary=media_tags, back_populates="tags")
```

**分类模型** (`app/models/category.py`):
```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func

from app.db.base import Base


class TagCategory(Base):
    __tablename__ = "tag_categories"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    key = Column(String(50), nullable=False, unique=True)
    label = Column(String(100), nullable=False)
    emoji = Column(String(10), nullable=False)
    color = Column(String(50), nullable=False)
    built_in = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
```

### 3. 数据库初始化

数据库会在应用启动时自动创建。SQLite 数据库文件位于项目根目录的 `media.db`。

## 五、安全与性能

### 1. 安全措施

- **输入验证**：使用 Pydantic 进行请求数据验证
- **文件上传安全**：验证文件类型和大小
- **路径遍历防护**：防止路径遍历攻击
- **CORS 配置**：允许跨域请求

### 2. 性能优化

- **数据库查询优化**：使用 SQLAlchemy 索引
- **文件处理**：优化文件上传和存储
- **API 响应**：使用适当的状态码和响应格式

## 六、部署指南

### 1. 生产环境配置

**环境变量**：
- `ENVIRONMENT=production`
- `PORT=8000`
- `HOST=0.0.0.0`

**服务配置**：
- 使用 uvicorn 作为 ASGI 服务器
- 建议使用 Nginx 作为反向代理（可选）

### 2. 部署流程

**本地生产部署**：
```bash
# 安装依赖
pip install -r requirements.txt

# 启动服务
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4
```

### 3. 日志管理

- 应用日志输出到控制台
- 建议配置日志文件存储（可选）

## 七、测试与维护

### 1. 测试覆盖率要求
- 单元测试：核心功能
- 集成测试：API 端点

### 2. 测试命令

```bash
# 安装测试依赖
pip install -r requirements-dev.txt

# 运行测试
pytest
```

### 3. 代码规范
- 遵循 PEP8 规范
- 使用 Black 进行代码格式化
- 使用 isort 进行导入排序
- 使用 flake8 进行代码质量检查

### 4. 版本控制
- 使用 Git 进行版本控制
- 建议使用分支策略：main (生产)、dev (开发)

### 5. 维护与更新说明
- **数据备份**：定期备份 `media.db` 文件
- **依赖更新**：定期更新依赖包
- **代码更新**：遵循代码规范，添加适当的注释

## 八、附录

### 1. 第三方库文档链接
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://docs.sqlalchemy.org/)
- [Pydantic](https://docs.pydantic.dev/)
- [Uvicorn](https://www.uvicorn.org/)

### 2. 常见问题与解决方案

**Q: 数据库文件丢失怎么办？**
A: 从备份中恢复 `media.db` 文件。

**Q: API 调用失败怎么办？**
A: 检查后端服务是否运行，检查网络连接，查看服务日志。

**Q: 文件上传失败怎么办？**
A: 检查文件大小，确保 `MEDIA_DIR` 和 `UPLOAD_DIR` 目录存在且可写。

### 3. 贡献指南

1. Fork 项目仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开 Pull Request

## 九、总结

本后端服务提供了一个完整的多维媒体管理系统的 API 接口，支持媒体文件管理、标签系统和标签分类管理。使用 FastAPI 和 SQLite 构建，适合个人本地使用。

服务具有以下特点：
- 轻量级：使用 SQLite 数据库，无需额外服务
- 高性能：FastAPI 框架提供高性能的 API 响应
- 易于部署：简单的环境配置和启动命令
- 安全可靠：完善的输入验证和错误处理

通过本后端服务，前端应用可以实现数据持久化存储，提供更稳定和可靠的用户体验。