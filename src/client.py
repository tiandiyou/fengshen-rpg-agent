#!/usr/bin/env python3
"""Claude SDK 客户端"""

from claude_code_sdk import ClaudeAgent


def create_client(model='claude-sonnet-4-5-20250929'):
    """创建 Claude Agent 客户端"""
    
    # 从环境变量获取 API Key
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        raise ValueError("请设置 ANTHROPIC_API_KEY 环境变量")
    
    # 创建客户端
    client = ClaudeAgent(
        model=model,
        api_key=api_key,
    )
    
    return client


import os
