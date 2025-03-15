from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from . import views

router = DefaultRouter()
router.register(r'projects', views.ProjectViewSet, basename='project')
project_router = NestedDefaultRouter(router, r'projects', lookup='project')
project_router.register(r'tasks', views.TaskViewSet, basename='project-tasks')
member_router = NestedDefaultRouter(router, r'projects', lookup='project')
member_router.register(r'members', views.ProjectMemberViewSet, basename='project-members')
router.register(r'tasks', views.TaskViewSet, basename='tasks')
task_router = NestedDefaultRouter(router, r'tasks', lookup='task')
task_router.register(r'comments', views.CommentViewSet, basename='task-comments')
router.register(r'comments', views.CommentViewSet, basename='comment')

urlpatterns = [
    path('users/register/', views.UserRegisterAPI.as_view(), name='register-user'),
    path('users/login/', views.UserLoginAPI.as_view(), name='login-user'),
    path('users/<int:id>/', views.UserAPI.as_view()),
    path('', include(router.urls)),
    path('', include(project_router.urls)),
    path('', include(member_router.urls)),
    path('', include(task_router.urls)),
]
