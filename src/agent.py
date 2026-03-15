#!/usr/bin/env python3
"""游戏 Agent 核心逻辑"""

import json
import os
import subprocess
import time
from pathlib import Path
from datetime import datetime

from claude_code_sdk import ClaudeAgent
from client import create_client
from progress import load_progress, save_progress
from prompts import load_prompt


class GameAgent:
    def __init__(self, project_dir, model, max_iterations=None, resume=False):
        self.project_dir = Path(project_dir)
        self.model = model
        self.max_iterations = max_iterations
        self.resume = resume
        self.client = None
        self.task_list_path = self.project_dir / 'task_list.json'
        
    def run(self):
        """运行 Agent"""
        # 初始化客户端
        self.client = create_client(self.model)
        
        # 检查是否恢复模式
        if self.resume and self.task_list_path.exists():
            self._resume_session()
        else:
            self._start_new_session()
    
    def _start_new_session(self):
        """开始新会话"""
        print("📋 阶段 1: 初始化 - 生成任务清单")
        print("-" * 40)
        
        # 加载初始提示词
        init_prompt = load_prompt('initializer_prompt.md')
        
        # 读取游戏策划案
        game_spec = Path(__file__).parent.parent / 'prompts' / 'game_spec.txt'
        if game_spec.exists():
            game_spec_content = game_spec.read_text()
            init_prompt = init_prompt.replace('{game_spec}', game_spec_content)
        
        # 调用 Agent 生成任务清单
        response = self.client.send_message(init_prompt)
        
        # 解析任务清单（从响应中提取 JSON）
        task_list = self._parse_task_list(response)
        
        # 保存任务清单
        save_progress(self.task_list_path, task_list)
        
        # 初始化 Git 仓库
        self._init_git()
        
        print(f"\n✅ 已生成 {len(task_list)} 个任务")
        print(f"📁 任务清单已保存到: {self.task_list_path}")
        
        # 开始执行任务
        self._run_coding_loop(task_list)
    
    def _resume_session(self):
        """从中断处恢复"""
        print("🔄 恢复上次会话...")
        
        # 加载任务清单
        task_list = load_progress(self.task_list_path)
        
        # 获取已完成的任务
        completed = [t for t in task_list if t.get('status') == 'completed']
        remaining = [t for t in task_list if t.get('status') != 'completed']
        
        print(f"📊 已完成: {len(completed)}, 剩余: {len(remaining)}")
        
        # 继续执行
        self._run_coding_loop(task_list)
    
    def _run_coding_loop(self, task_list):
        """执行任务循环"""
        print("\n📋 阶段 2: 执行任务")
        print("-" * 40)
        
        iteration = 0
        while True:
            # 检查最大迭代
            if self.max_iterations and iteration >= self.max_iterations:
                print(f"\n✅ 达到最大迭代次数 ({self.max_iterations})")
                break
            
            # 找到下一个未完成的任务
            next_task = None
            for task in task_list:
                if task.get('status') != 'completed':
                    next_task = task
                    break
            
            if not next_task:
                print("\n🎉 所有任务已完成！")
                break
            
            iteration += 1
            print(f"\n[{iteration}] 执行任务: {next_task['name']}")
            
            # 加载编码提示词
            coding_prompt = load_prompt('coding_prompt.md')
            coding_prompt = coding_prompt.replace('{current_task}', json.dumps(next_task, ensure_ascii=False, indent=2))
            coding_prompt = coding_prompt.replace('{project_dir}', str(self.project_dir))
            
            # 获取已完成任务列表
            completed_tasks = [t for t in task_list if t.get('status') == 'completed']
            coding_prompt = coding_prompt.replace(
                '{completed_tasks}', 
                json.dumps(completed_tasks, ensure_ascii=False, indent=2)
            )
            
            # 调用 Agent 执行任务
            response = self.client.send_message(coding_prompt)
            
            # 更新任务状态
            next_task['status'] = 'completed'
            next_task['completed_at'] = datetime.now().isoformat()
            next_task['result'] = response[:500]  # 保存部分结果
            
            # 保存进度
            save_progress(self.task_list_path, task_list)
            
            # Git 提交
            self._git_commit(f"完成: {next_task['name']}")
            
            print(f"✅ 任务完成: {next_task['name']}")
            
            # 等待后继续
            print("⏳ 3秒后继续下一个任务...")
            time.sleep(3)
    
    def _parse_task_list(self, response):
        """从响应中解析任务清单"""
        import re
        
        # 尝试提取 JSON
        json_match = re.search(r'```json\s*(.*?)\s*```', response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except:
                pass
        
        # 尝试直接解析
        try:
            return json.loads(response)
        except:
            # 返回默认任务清单
            return [
                {"id": 1, "name": "创建游戏基础结构", "status": "pending", "priority": "high"},
                {"id": 2, "name": "实现标题界面", "status": "pending", "priority": "high"},
                {"id": 3, "name": "实现剧情系统", "status": "pending", "priority": "high"},
                {"id": 4, "name": "实现战斗系统", "status": "pending", "priority": "high"},
                {"id": 5, "name": "实现角色系统", "status": "pending", "priority": "medium"},
            ]
    
    def _init_git(self):
        """初始化 Git 仓库"""
        if not (self.project_dir / '.git').exists():
            subprocess.run(['git', 'init'], cwd=self.project_dir, capture_output=True)
            subprocess.run(['git', 'add', '.'], cwd=self.project_dir, capture_output=True)
            subprocess.run(
                ['git', 'commit', '-m', 'Initial commit: 封神榜游戏项目'],
                cwd=self.project_dir, 
                capture_output=True
            )
            print("📦 Git 仓库已初始化")
    
    def _git_commit(self, message):
        """Git 提交"""
        subprocess.run(['git', 'add', '.'], cwd=self.project_dir, capture_output=True)
        result = subprocess.run(
            ['git', 'commit', '-m', message],
            cwd=self.project_dir,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"📦 已提交: {message}")
