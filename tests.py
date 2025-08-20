import os
import re
import django

# 设置 Django 配置
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from devops.models import Script

script_path = os.path.join(os.path.dirname(__file__), 'devops', 'script')

for script_file in os.listdir(script_path):
    full_path = os.path.join(script_path, script_file)
    if not os.path.isfile(full_path):
        continue
    script_type = 'python3'
    if script_file.endswith('.sh'):
        script_type = 'bash'
    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()
        param_count = len(re.findall(r'sys\.argv', content))
        print(f"{script_file}: param_count = {param_count}")

        # 查询是否已存在该脚本
        script = Script.objects.filter(name=script_file).first()

        if script:
            print('update')
            updated = False
            if script.param_count != param_count:
                script.param_count = param_count
                updated = True
                print('param_count not equal, updating...')

            if script.content != content:
                script.content = content
                updated = True
                print('content not equal, updating...')

            if script.script_type != script_type:
                script.script_type = script_type
                updated = True
                print('script_type not equal, updating...')

                

            if updated:
                script.save()
                print('Updated.')
            else:
                print('No changes.')
        else:
            # 创建新脚本
            Script.objects.create(name=script_file, param_count=param_count, content=content)
            print('create')
