#!/usr/bin/env python3
"""
封神榜 - 伐商演义
长时间运行 RPG 游戏开发框架
基于 Claude Agent SDK
"""

import argparse
import os
import sys
from pathlib import Path

# 添加 src 目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from agent import GameAgent


def main():
    parser = argparse.ArgumentParser(description='封神榜游戏开发 Agent')
    parser.add_argument(
        '--project-dir',
        type=str,
        default='./fengshen_project',
        help='项目目录'
    )
    parser.add_argument(
        '--max-iterations',
        type=int,
        default=None,
        help='最大迭代次数（用于测试）'
    )
    parser.add_argument(
        '--model',
        type=str,
        default='claude-sonnet-4-5-20250929',
        help='Claude 模型'
    )
    parser.add_argument(
        '--resume',
        action='store_true',
        help='从上次中断处继续'
    )
    
    args = parser.parse_args()
    
    # 确保项目目录存在
    project_dir = Path(args.project_dir)
    project_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"🚀 启动封神榜游戏开发 Agent")
    print(f"📁 项目目录: {project_dir}")
    print(f"🤖 模型: {args.model}")
    if args.max_iterations:
        print(f"🔄 最大迭代: {args.max_iterations}")
    print()
    
    # 创建并运行 Agent
    agent = GameAgent(
        project_dir=str(project_dir),
        model=args.model,
        max_iterations=args.max_iterations,
        resume=args.resume
    )
    
    try:
        agent.run()
    except KeyboardInterrupt:
        print("\n\n⏸️ 已暂停运行")
        print("再次运行相同命令可继续执行")
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        raise


if __name__ == '__main__':
    main()
