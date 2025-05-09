#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
u0645u0644u0641 u062au0643u0648u064au0646 u0644u0648u0643u064au0644 u0642u0627u0626u0645u0629 u0627u0644u0645u0647u0627u0645
"""

# u0625u0639u062fu0627u062fu0627u062a u0642u0627u0639u062fu0629 u0627u0644u0628u064au0627u0646u0627u062a
DB_CONFIG = {
    "host": "127.0.0.1",  # الاتصال بالمحلي بدلاً من docker
    "port": 3306,
    "user": "root",
    "password": "2452329511",  # كلمة المرور الحالية
    "database": "windsurf_pro_hours"  # اسم قاعدة البيانات الحالية
}

# u0625u0639u062fu0627u062fu0627u062a u0627u0644u0648u0643u064au0644
AGENT_CONFIG = {
    "memory_file": "agent_memory.json",  # u0645u0644u0641 u0627u0644u0630u0627u0643u0631u0629 u0637u0648u064au0644u0629 u0627u0644u0645u062fu0649
    "todo_file": "README.md",          # u0645u0644u0641 u0642u0627u0626u0645u0629 u0627u0644u0645u0647u0627u0645
    "log_level": "INFO",               # u0645u0633u062au0648u0649 u0627u0644u062au0633u062cu064au0644
    "auto_save": True                  # u062du0641u0638 u062au0644u0642u0627u0626u064a u0644u0644u062au063au064au064au0631u0627u062a
}
