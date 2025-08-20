from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('create/', views.create, name='create'),
    path("<int:post_id>/update/", views.update, name="update"),
    path("<int:post_id>/delete", views.delete, name="delete"),

    path('script_list/', views.script_list, name='script_list'),
    # 根据脚本ID执行脚本
    path('scripts/run/<int:script_id>/', views.run_script, name='run_script'),
    path('get_fun_status/', views.get_fun_status, name='get_fun_status'),
    path('select_error_ratio/', views.select_error_ratio, name='select_error_ratio'),
    path('update_script/<int:script_id>/', views.update_script, name='update_script'),
    path('delete_script/<int:script_id>/', views.delete_script, name='delete_script'),
    path('create_script/', views.create_script, name='create_script'),

    
]
