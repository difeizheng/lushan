# 庐山文旅通 - 庐山文化旅游信息平台

🏞️ 基于 Streamlit 构建的庐山旅游信息服务平台

## 项目简介

本项目是一个集信息查询、导览服务、文化展示、行程规划于一体的庐山旅游服务平台。
通过 Streamlit 快速构建，无需复杂的前后端分离架构，即可实现美观实用的 Web 应用。

## 功能特性

### 🏞️ 景点导览
- 景点列表展示，支持分类筛选
- 景点详细信息，包括海拔、游览时间、难度等
- 搜索功能，快速找到目标景点

### 📚 文化百科
- 历史沿革时间线展示
- 名人堂：李白、白居易、苏轼等与庐山有关的名人
- 诗词库：收录 4000+ 首与庐山相关的诗词

### 🗺️ 行程规划
- 预设路线：一日游、二日游、三日游
- 主题路线：诗词文化之旅、宗教文化之旅、登山爱好者路线
- 自定义行程规划工具

### 🗺️ 地图导览
- 景点坐标展示
- 图层筛选（分类、难度）
- 数据导出（CSV、JSON）

### 🛠️ 实用信息
- 天气气候信息
- 交通指南
- 门票信息
- 紧急联系方式

## 快速开始

### 环境要求

- Python 3.9+
- pip 包管理器

### 安装依赖

```bash
cd lushan
pip install -r requirements.txt
```

### 运行应用

```bash
streamlit run app.py
```

应用将在 `http://localhost:8503` 启动。

### 部署到 Streamlit Cloud

1. 将项目推送到 GitHub
2. 访问 [Streamlit Cloud](https://share.streamlit.io/)
3. 连接 GitHub 仓库
4. 选择 `app.py` 作为主文件
5. 点击部署

## 项目结构

```
lushan/
├── app.py                  # 主应用文件（首页）
├── requirements.txt        # 依赖配置
├── README.md              # 项目说明
├── 系统功能规划.md         # 功能规划文档
├── data/                  # 数据目录
│   ├── scenic_spots.yml   # 景点数据
│   ├── celebrities.yml    # 名人数据
│   ├── poems.yml          # 诗词数据
│   └── routes.yml         # 路线数据
├── pages/                 # 页面目录
│   ├── 01_🏞️_景点导览.py
│   ├── 02_📚_文化百科.py
│   ├── 03_🗺️_行程规划.py
│   ├── 04_🗺️_地图导览.py
│   └── 05_🛠️_实用信息.py
└── utils/                 # 工具模块
    └── __init__.py
```

## 数据说明

项目数据存储在 `data/` 目录下，采用 YAML 格式：

- `scenic_spots.yml`: 景点数据（名称、分类、位置、描述等）
- `celebrities.yml`: 名人数据（姓名、朝代、身份、简介等）
- `poems.yml`: 诗词数据（标题、作者、内容、创作背景等）
- `routes.yml`: 路线数据（路线名称、时长、难度、景点列表等）

## 扩展开发

### 添加新景点

编辑 `data/scenic_spots.yml`，添加新的景点记录：

```yaml
- id: 13
  name: 新景点名称
  category: 自然景观
  subcategory: 山峰
  altitude: 1200
  description: 景点描述
  location:
    lat: 29.55
    lng: 116.05
  tags: [标签 1, 标签 2]
  visiting_time: 1-2 小时
  difficulty: 简单
```

### 添加新页面

在 `pages/` 目录下创建新的 Python 文件，文件名格式为：
`序号_图标_页面名称.py`

例如：`06_📷_摄影指南.py`

### 自定义样式

编辑 `app.py` 中的 CSS 样式部分，或创建独立的主题文件。

## 技术栈

- **框架**: Streamlit 1.32+
- **语言**: Python 3.9+
- **数据处理**: Pandas
- **数据格式**: YAML
- **部署**: Streamlit Cloud / Docker / 本地服务器

## 截图预览

（此处可添加应用截图）

## 贡献指南

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License

---

**开发日期**: 2026 年 3 月 24 日
**版本**: v1.0.0
