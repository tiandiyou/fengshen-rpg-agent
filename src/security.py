#!/usr/bin/env python3
"""安全沙箱 - 命令白名单"""

# 允许的命令列表
ALLOWED_COMMANDS = {
    # 文件查看
    'ls', 'cat', 'head', 'tail', 'wc', 'grep', 'find', 'tree',
    # Node.js
    'npm', 'node',
    # 版本控制
    'git',
    # 进程管理
    'ps', 'lsof', 'sleep', 'pkill',
    # Python
    'python', 'python3', 'pip',
}

# 允许的文件操作目录
ALLOWED_DIRS = ['.', '..']


def is_command_allowed(cmd):
    """检查命令是否允许执行"""
    import shlex
    try:
        args = shlex.split(cmd)
        if args:
            command = args[0]
            return command in ALLOWED_COMMANDS
    except:
        pass
    return False
