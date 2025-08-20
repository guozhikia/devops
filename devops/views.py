# test1/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
import subprocess
import os
from .models import Post
from .models import User
from .models import Script
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from datetime import datetime

def index(request):
    posts = Post.objects.all()
    return render(request, 'devops/base.html', {'posts': posts})

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.create(
            username=username, 
            password=password)
        return redirect('index')
    return render(request, 'devops/register.html')

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(f"尝试登录用户: {username}，密码: {password}") 
        try:
            # all_users = User.objects.all()  # 获取所有用户，QuerySet
            # print(all_users)  
            user = User.objects.get(username=username)
            print(f"查到用户: {user.username}")
        except User.DoesNotExist:
            user = None
            messages.error(request, "用户不存在!")
            return render(request, 'devops/login.html')

        if user is not None:
            print(user.password)
            print(password)
            if password == user.password:
                request.session['user_id'] = user.id  # 记录当前登录的用户
                request.session['username'] = user.username
                messages.success(request, "登录成功！")
                # return redirect('create')
                return redirect('index')
            else:
                messages.error(request, "密码不正确!")

    return render(request, 'devops/login.html')


def logout(request):
    request.session.flush()
    messages.success(request, "您已成功退出登录！")
    return redirect('login')


def create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        body = request.POST.get('body')
        error = None
        if not title:
            error = '标题不能为空'
            return HttpResponse(error)
        elif not body:
            error = '内容不能为空'
            return HttpResponse(error)
        else:
            try:
                user_id = request.session['user_id']
                user = User.objects.get(id=user_id) # 匹配用户 id 来获取 User 实例
            except KeyError:
                # session 中没有 user_id
                return HttpResponse("未登录，请先登录。访问地址：http://10.170.142.201:8001/devops/login/", status=401)
                # return redirect('/login/')
            post = Post(title=title, body=body, author=user)
            post.save()  # 保存到数据库
            messages.success(request, "创建成功！")
            return redirect('index')
        
    return render(request, 'devops/create.html')

def update(request, post_id):
    # 使用django的 get_object_or_404() 函数来获取要更新的文章,如果不存在改成404
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        title = request.POST.get("title")
        body = request.POST.get("body")

        error = None
        if not title:
            error = '标题不能为空'
            return HttpResponse(error)
        elif not body:
            error = '内容不能为空'
            return HttpResponse(error)
        else:
            ## 更新博客内容
            post.title = title
            post.body = body
            post.save() ## 保存到数据里
            return redirect('index')

    return render(request, 'devops/update.html', {'post': post})


def delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect('index')




# def script_list(request):
#     scripts = Script.objects.all()
#     return render(request, 'devops/script_list.html', {'scripts': scripts})

def script_list(request):
    scripts = Script.objects.all()

    return render(request, 'devops/script_list.html', {'scripts': scripts})


def run_script(request, script_id):
    output = ''
    script = get_object_or_404(Script, id=script_id)
    script_name = script.name.split('.')[0]

    print(request.method)
    print(request.method)
    print(request.method)
    if request.method == 'POST':
        param1 = request.POST.get("param1", "")
        param2 = request.POST.get("param2", "")
        # error = None

        print(script.param_count)
        print(type(script.param_count))
        # 这里假设 script.content 是 shell 脚本的完整字符串

        try:
            # 使用 subprocess 运行脚本内容
            # echo 脚本内容通过管道传入 bash 执行
            if script.param_count == 0:
                output = subprocess.run(
                    [script.script_type, '-c', script.content],
                    capture_output=True,
                    text=True,
                    timeout=600  # 限制执行时间，防止死循环
                )
            elif script.param_count == 1:
                output = subprocess.run(
                    [script.script_type, '-c', script.content, param1,],
                    capture_output=True,
                    text=True,
                    timeout=600  # 限制执行时间，防止死循环
                )
            elif script.param_count == 2:
                output = subprocess.run(
                    [script.script_type, '-c', script.content, param1, param2],
                    capture_output=True,
                    text=True,
                    timeout=600  # 限制执行时间，防止死循环
                )
            else:
                error = '参数数量错误！'
                return render(request, f'devops/run_script.html', {'error': error, 'script': script})
            

            print(output)
            result = output.stdout  # subprocess.run with text=True，输出在stdout
            error = output.stderr  # subprocess.run with text=True，错误输出在stderr
            print("==================================")
            print(output)
            print("\++++++++++++++++++++++++++++++++++++++")
            print(error)

            if error:
                return render(request, f'devops/run_script.html', {'result': result, 'error': error, 'script': script})
            else:
                return render(request, f'devops/run_script.html', {'result': result, 'script': script})
        
        
        except subprocess.TimeoutExpired:
            error = '脚本执行超时！'
            return render(request, f'devops/run_script.html', {'error': error, 'script': script})
        except Exception as e:
            error = f'执行异常: {str(e)}'
            return render(request, f'devops/run_script.html', {'error': error,'script': script})

    else:
        return render(request, f'devops/run_script.html', {'script': script})   


def update_script(request, script_id):
    script = get_object_or_404(Script, id=script_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        content = request.POST.get('content')
        param_count = request.POST.get('param_count')
        script_type = request.POST.get('script_type')
        exec_cmd = request.POST.get('exec_cmd')

        script.name = name
        script.content = content
        script.param_count = param_count
        script.script_type = script_type
        script.exec_cmd = exec_cmd
        script.updated = datetime.now()
        script.save()
        messages.success(request, "更新成功！")
        return redirect('script_list')
    else:
        return render(request, 'devops/update_script.html', {'script': script})


def delete_script(request, script_id):
    print(request.method)
    if request.method == 'POST':
        script = get_object_or_404(Script, id=script_id)
        script.delete()
        return redirect('script_list')
    else:
        return render(request, 'devops/delete_script.html', {'script': script})

def create_script(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        content = request.POST.get('content')
        param_count = request.POST.get('param_count')
        script_type = request.POST.get('script_type')

        script = Script(name=name, content=content, param_count=param_count, script_type=script_type)
        script.save()

        return redirect('script_list')
    else:
        return render(request, 'devops/create_script.html')


def select_error_ratio(request):
    result = ''
    error = ''
    name = request.GET.get('name')
    city = request.GET.get('city')

    if name and city:
        try:
            # 获取脚本的绝对路径
            script_path = os.path.join(os.path.dirname(__file__), 'script', 'select_error_ratio.py')

            # 执行脚本并传参
            output = subprocess.check_output(
                ['python3', script_path, name, city],
                stderr=subprocess.STDOUT,
                timeout=1000
            )
            result = output.decode('utf-8')
            print(result)

        except subprocess.CalledProcessError as e:
            error = e.output.decode('utf-8')
        except Exception as e:
            error = str(e)

    return render(request, 'devops/select_error_ratio.html', {'result': result, 'error': error})



def get_fun_status(request):
    result = ''
    error = ''
    plan_id = request.GET.get('plan_id')
    if plan_id:
        try:
            # 获取脚本的绝对路径
            script_path = os.path.join(os.path.dirname(__file__), 'script', 'get_fun_status.py')

            # 执行脚本并传参
            output = subprocess.check_output(
                ['python3', script_path, plan_id],
                stderr=subprocess.STDOUT,
                timeout=1000
            )
            result = output.decode('utf-8')

        except subprocess.CalledProcessError as e:
            error = e.output.decode('utf-8')
        except Exception as e:
            error = str(e)

    return render(request, 'devops/get_fun_status.html', {'result': result, 'error': error})
