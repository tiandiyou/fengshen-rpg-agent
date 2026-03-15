#!/usr/bin/env python3
"""提示词加载工具"""

from pathlib import Path


def load_prompt(name):
    """加载提示词文件"""
    prompt_dir = Path(__file__).parent.parent / 'prompts'
    prompt_path = prompt_dir / name
    
    if not prompt_path.exists():
        return ""
    
    return prompt_path.read_text(encoding='utf-8')
