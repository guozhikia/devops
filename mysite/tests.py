# from django.test import TestCase

# Create your tests here.


import os
import django

# from models import Script

# 设置环境变量，指向你的 Django 项目 settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'devops.settings')  

# 初始化 Django
django.setup()

from devops.models import Script  # 这里改成你的app名字

script_path = os.path.join(os.path.dirname(__file__), 'script', 'select_error_ratio.py')
# script_path = "/path/to/your/script/select_error_ratio.py"
with open(script_path, 'r', encoding='utf-8') as f:
    content = f.read()

Script.objects.create(name="select_error_ratio.py", content=content)
print("脚本已写入数据库")

