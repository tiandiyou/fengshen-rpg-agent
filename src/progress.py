#!/usr/bin/env python3
"""进度跟踪工具"""

import json
from pathlib import Path


def load_progress(task_list_path):
    """加载任务进度"""
    if not task_list_path.exists():
        return []
    
    content = task_list_path.read_text(encoding='utf-8')
    return json.loads(content)


def save_progress(task_list_path, task_list):
    """保存任务进度"""
    content = json.dumps(task_list, ensure_ascii=False, indent=2)
    task_list_path.write_text(content, encoding='utf-8')
