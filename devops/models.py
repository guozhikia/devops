from enum import unique
from django.db import models
from django.utils import timezone


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    body = models.TextField()

    def __str__(self):
        return self.title

class Script(models.Model):
    name = models.CharField(max_length=100, unique=True)
    content = models.TextField()
    param_count = models.PositiveIntegerField(default=0)
    script_type = models.CharField(max_length=50, default='python3') 
    exec_cmd = models.CharField(max_length=500) 
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # def save(self, *args, **kwargs):
    #     try:
    #         existing = Script.objects.get(name=self.name)
    #         if existing.content != self.content:
    #             self.id = existing.id  # 更新这条记录而不是新增
    #             self.updated = timezone.now()
    #             super().save(*args, **kwargs)
    #             print("脚本已更新")
    #         else:
    #             # 内容相同，不更新
    #             print("内容相同，不更新")
    #             pass
    #     except Script.DoesNotExist:
    #         # 不存在同名记录，正常保存
    #         super().save(*args, **kwargs)

    def __str__(self):
        return self.name
