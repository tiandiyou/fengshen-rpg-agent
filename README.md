# 封神榜 - 伐商演义

基于 Claude Agent SDK 的长时间运行 RPG 游戏开发框架。

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 设置 API Key

```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

### 3. 运行

```bash
python src/game_agent.py --project-dir ./fengshen_project
```

### 4. 测试运行（限制迭代次数）

```bash
python src/game_agent.py --project-dir ./fengshen_project --max-iterations 3
```

## 框架说明

- **Initializer Agent**: 读取 game_spec.txt，生成 task_list.json 任务清单
- **Coding Agent**: 逐个实现任务，更新进度，支持中断恢复
- **进度持久化**: 通过 task_list.json + git 保存

## 项目结构

```
fengshen-rpg-agent/
├── src/
│   ├── game_agent.py      # 主入口
│   ├── agent.py           # Agent 会话逻辑
│   ├── client.py          # Claude SDK 客户端
│   ├── security.py       # 安全沙箱
│   ├── progress.py       # 进度跟踪
│   └── prompts.py        # 提示词加载
├── prompts/
│   ├── game_spec.txt      # 游戏策划案
│   ├── initializer_prompt.md
│   └── coding_prompt.md
├── requirements.txt
└── README.md
```
