from django.db.models import QuerySet
from rest_framework import status, views, viewsets, permissions
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework_simplejwt.tokens import RefreshToken
from pms import models
from . import serializers
from .response import APIResponse
from utils import messages as msg, exceptions


class UserRegisterAPI(views.APIView):
    
    def post(self, request: Request) -> Response:
        serializer = serializers.UserSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            models.User.objects.create(**request.data)
            print('user created')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class UserLoginAPI(views.APIView):
    
    def post(self, request: Request) -> Response:
        username = request.data.get('username')
        password = request.data.get('password')
        authenticated, message = models.User.authenticate(username, password)
        if authenticated:
            user = models.User.objects.get(username=username)
            refresh_token = RefreshToken.for_user(user)
            return Response(
                APIResponse(
                    refresh_token=str(refresh_token), access_token=str(refresh_token.access_token)).__dict__, 
                status=status.HTTP_200_OK)
        return Response(APIResponse(**message).__dict__, status=status.HTTP_401_UNAUTHORIZED)
            

class UserAPI(views.APIView):
    # permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request: Request, id: int) -> Response:
        user = models.User.objects.filter(id=id).first()
        if user is not None:
            serializer = serializers.UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            APIResponse(id=[msg.NOT_FOUND]).__dict__, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request: Request, id: int) -> Response:
        user = models.User.objects.filter(id=id).first()
        if user is not None:
            partial = request.method == 'PATCH'
            serializer = serializers.UserSerializer(
                user, data=request.data, partial=partial)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            APIResponse(id=[msg.NOT_FOUND]).__dict__, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request: Request, id: int) -> Response:
        user = models.User.objects.filter(id=id).first()
        if user is not None:
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            APIResponse(id=[msg.NOT_FOUND]).__dict__, status=status.HTTP_404_NOT_FOUND)


class ProjectViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated]
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer
    
    
class ProjectMemberViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.ProjectMemberSerializer
    
    def handle_exception(self, exc):
        """
        Making sure if the exception is for the unique constraint then
        a more comprehensive error message is shown as API response
        """
        if exceptions.NON_FIELD_ERRORS in str(exc).lower():
            return Response(
                APIResponse(
                    duplicate_error=msg.DUPLICATE_PROJECT_MEMBER).__dict__, 
                status=status.HTTP_400_BAD_REQUEST)
        return super().handle_exception(exc)
    
    def get_queryset(self) -> QuerySet:
        pk = 'project_pk'
        if pk in self.kwargs:
            return models.ProjectMember.objects.filter(project_id=self.kwargs[pk])
        return models.ProjectMember.objects.all()
    
    
class TaskViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.TaskSerializer
    
    def handle_exception(self, exc):
        """
        returing an appropriate error message if a Task is assigned
        to some user who is not a member of the same project
        """
        if msg.NOT_PROJECT_MEMBER_ERROR in str(exc):
            return Response(
                APIResponse(
                    not_project_member_error=msg.NOT_PROJECT_MEMBER_ERROR).__dict__, 
                status=status.HTTP_400_BAD_REQUEST)
        return super().handle_exception(exc)
    
    def get_queryset(self) -> QuerySet:
        pk = 'project_pk'
        if pk in self.kwargs:
            return models.Task.objects.filter(project_id=self.kwargs[pk])
        return models.Task.objects.all()
    
    
class CommentViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.CommentSerializer
    
    def get_queryset(self) -> QuerySet:
        pk = 'task_pk'
        if pk in self.kwargs:
            return models.Comment.objects.filter(task_id=self.kwargs[pk])
        return models.Comment.objects.all()
    
    