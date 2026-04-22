# Data Agent - 智能数据查询系统

基于 LangGraph 和 RAG 技术的智能数据查询系统，通过自然语言问答自动生成并执行 SQL 查询。

## 项目简介

Data Agent 是一个智能数据分析助手，能够理解用户的自然语言问题，自动从元数据知识库中检索相关信息，生成准确的 SQL 查询语句，并返回查询结果。系统采用多阶段处理流程，包括关键词提取、信息召回、SQL 生成、验证和执行等步骤。

### 核心特性

- 🤖 自然语言转 SQL：支持中文自然语言查询
- 🔍 智能信息检索：基于向量数据库的语义检索
- 📊 多维度数据分析：支持维度表和事实表的复杂查询
- ✅ SQL 验证与纠错：自动验证和修正生成的 SQL
- 🎯 流式响应：实时展示查询进度和结果
- 🌐 Web 界面：简洁友好的前端交互界面

## 技术栈

### 后端
- **FastAPI**: Web 框架
- **LangGraph**: Agent 工作流编排
- **LangChain**: LLM 应用开发框架
- **Qdrant**: 向量数据库（字段和指标检索）
- **Elasticsearch**: 全文搜索引擎（字段取值检索）
- **MySQL**: 关系型数据库（元数据和数据仓库）
- **HuggingFace TEI**: 文本嵌入服务

### 前端
- **Vue 3**: 前端框架
- **Vite**: 构建工具

## 系统架构

```
用户问题 → 关键词提取 → 并行召回（字段/指标/取值）→ 信息合并 
  → 过滤（指标/表）→ 添加额外上下文 → 生成SQL → 验证SQL 
  → 执行SQL → 返回结果
```

## 快速开始

### 环境要求

- Python >= 3.12
- Node.js >= 16
- Docker & Docker Compose
- uv (Python 包管理器)

### 1. 启动基础服务

使用 Docker Compose 启动所有依赖服务：

```bash
cd docker
docker-compose up -d
```

这将启动以下服务：
- MySQL (端口 3307)
- Elasticsearch (端口 9200)
- Kibana (端口 5601)
- Qdrant (端口 6333)
- Embedding Service (端口 8081)

### 2. 配置文件

编辑 `conf/app_config.yaml` 配置数据库连接和 LLM 信息：

```yaml
llm:
  model_name: gpt-4  # 修改为你的模型
  api_key: your-api-key  # 修改为你的 API Key
  base_url: https://api.openai.com/v1  # 修改为你的 API 地址
```

编辑 `conf/meta_config.yaml` 定义你的数据模型（表结构、字段、指标等）。

### 3. 初始化元数据

构建元数据知识库：

```bash
# 创建虚拟环境并安装依赖
uv venv
source .venv/Scripts/activate  # Windows: .venv\Scripts\activate

# 安装依赖
uv pip install -e .

# 清理并重建知识库
python clean_and_rebuild.py
```

### 4. 启动后端服务

```bash
fastapi dev main.py
```

后端服务将在 `http://127.0.0.1:8000` 启动。

API 文档：`http://127.0.0.1:8000/docs`

### 5. 启动前端服务

```bash
cd data-agent-fronted
npm install
npm run dev
```

前端服务将在 `http://localhost:5173` 启动。

## 项目结构

```
.
├── app/
│   ├── api/                    # API 路由和依赖
│   │   ├── routers/           # 路由定义
│   │   └── schemas/           # 请求/响应模型
│   ├── clients/               # 客户端管理器
│   │   ├── embedding_client_manager.py
│   │   ├── es_client_manager.py
│   │   ├── mysql_client_manager.py
│   │   └── qdrant_client_manager.py
│   ├── conf/                  # 配置加载
│   ├── core/                  # 核心功能（日志等）
│   ├── entities/              # 业务实体
│   ├── models/                # 数据库模型
│   ├── my_agent/              # Agent 核心逻辑
│   │   ├── nodes/            # 工作流节点
│   │   │   ├── extract_keywords.py      # 关键词提取
│   │   │   ├── recall_column.py         # 字段召回
│   │   │   ├── recall_metric.py         # 指标召回
│   │   │   ├── recall_value.py          # 取值召回
│   │   │   ├── merge_retrieved_info.py  # 信息合并
│   │   │   ├── filter_metric.py         # 指标过滤
│   │   │   ├── filter_table.py          # 表过滤
│   │   │   ├── add_extra_context.py     # 添加上下文
│   │   │   ├── generate_sql.py          # SQL 生成
│   │   │   ├── validate_sql.py          # SQL 验证
│   │   │   ├── correct_sql.py           # SQL 纠错
│   │   │   └── execute_sql.py           # SQL 执行
│   │   ├── graph.py          # LangGraph 工作流定义
│   │   ├── state.py          # 状态管理
│   │   └── context.py        # 上下文管理
│   ├── prompt/               # Prompt 模板
│   ├── repositories/         # 数据访问层
│   │   ├── es/              # Elasticsearch 仓储
│   │   ├── mysql/           # MySQL 仓储
│   │   └── qdrant/          # Qdrant 仓储
│   ├── scripts/             # 脚本工具
│   └── services/            # 业务服务层
├── conf/                    # 配置文件
│   ├── app_config.yaml     # 应用配置
│   └── meta_config.yaml    # 元数据配置
├── data-agent-fronted/     # 前端项目
│   ├── src/
│   │   ├── App.vue        # 主组件
│   │   └── main.js
│   └── vite.config.js
├── docker/                 # Docker 配置
│   ├── docker-compose.yaml
│   ├── elasticsearch/
│   ├── embedding/
│   └── mysql/
├── prompts/               # Prompt 模板文件
├── logs/                  # 日志目录
├── main.py               # 应用入口
├── clean_and_rebuild.py  # 重建知识库脚本
└── pyproject.toml        # Python 项目配置
```

## 使用示例

启动服务后，在前端界面输入自然语言问题：

- "华东地区的销售额是多少？"
- "查询2024年各品类的GMV"
- "哪个省份的订单量最高？"
- "计算平均订单金额"

系统会自动：
1. 提取关键词
2. 检索相关字段、指标和取值
3. 生成 SQL 查询
4. 验证并执行
5. 返回结果表格

## API 接口

### POST /api/query

查询接口，支持流式响应。

**请求体：**
```json
{
  "query": "华东地区的销售额是多少？"
}
```

**响应：** Server-Sent Events (SSE) 流

```
data: {"type": "progress", "step": "抽取关键词", "status": "running"}
data: {"type": "progress", "step": "抽取关键词", "status": "success"}
...
data: {"type": "result", "data": [{"region": "华东", "amount": 1000000}]}
```

## 配置说明

### 元数据配置 (meta_config.yaml)

定义数据模型结构：

```yaml
tables:
  - name: dim_region          # 表名
    role: dim                 # 角色：dim(维度表) / fact(事实表)
    description: 地区维度表   # 表描述
    columns:
      - name: region_id       # 字段名
        role: primary_key     # 角色：primary_key / foreign_key / dimension / measure
        description: 地区ID   # 字段描述
        alias: [地区ID, 区域ID]  # 别名
        sync: false           # 是否同步到向量库

metrics:
  - name: GMV                 # 指标名称
    description: 成交总额     # 指标描述
    relevant_columns:         # 相关字段
      - fact_order.order_amount
    alias: [成交总额, 订单总额]  # 别名
```

## 开发指南

### 添加新的处理节点

1. 在 `app/my_agent/nodes/` 创建新节点文件
2. 实现节点函数，接收和返回 `State` 对象
3. 在 `app/my_agent/graph.py` 中注册节点
4. 添加到工作流图中

### 自定义 Prompt

编辑 `prompts/` 目录下的 `.prompt` 文件，系统会自动加载。

### 扩展数据源

实现新的 Repository 类，继承相应的基类，并在 `clients/` 中添加客户端管理器。

## 常见问题

### Q: Docker 服务启动失败？
A: 检查端口是否被占用，可以修改 `docker-compose.yaml` 中的端口映射。

### Q: 向量检索结果不准确？
A: 调整 `meta_config.yaml` 中字段的 `sync` 配置，确保重要字段被索引。重新运行 `clean_and_rebuild.py`。

### Q: SQL 生成错误？
A: 检查 Prompt 模板，确保元数据描述清晰准确。可以在 `prompts/` 目录下调整相关模板。

### Q: 前端代理 501 错误？
A: 确保后端服务已启动，检查 `vite.config.js` 中的代理配置是否正确。

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 联系方式

如有问题或建议，请提交 Issue。
