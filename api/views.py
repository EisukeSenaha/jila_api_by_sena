from django.shortcuts import render
from rest_framework import status, permissions, generics, viewsets
from .serialisers import UserSerializer, CategorySerializer, TaskSerializer, ProfileSirializer
from rest_framework.response import Response
from .models import Task, Profile, Category
from django.contrib.auth.models import User
from . import custompermissions

# djangoのrest_frameworkにはgenericでつくるviewとmodelViewSetというviewがある
# modelViewSetはCRUDの各メゾットを提供しているが genericから始まるviewは特定のメゾット特化である
# viewの中にはシリアライザーを指定する
class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    # ユーザーをまだ作成していない場合JWTがないためVIEWにアクセスできない
    # これはsetting.pyでdefault_permissionとdefualt_authentificationで設定している
    # そのため誰でもこのviewにアクセスできるようオーバーライドして再設定する
    permission_classes = (permissions.AllowAny,)

class ListUserView(generics.ListAPIView):
    # オブジェクトの取得し表示するようなviewではquerysetにオブジェクトを格納する
    queryset = User.objects.all()
    serializer_class = UserSerializer

# GETメゾットでログインしているユーザーの情報を取得するようなviewを定義
# Retrieve => 特定のオブジェクトを検索して返してくれる
class LoginUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    # ログインしているユーザーオブジェクトの取得
    # get_objectをオーバーライドして取得する
    # request.user でログインしているユーザーにアクセスできる
    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        response = "you cant update here"
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

# modelViewSetを使ってCRUDに対応させる
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSirializer

    # CRUDのcreateメゾットをオーバーライドしてuser_profileにログインしているユーザーを格納して
    # フロントエンドでいちいちuser_profileと紐付け先の選定作業を取り除く
    def perform_create(self, serializer):
        serializer.save(user_profile=self.request.user)

    # 使わないメゾットを無効化する
    # deleteはdestoryメゾットとして用意されているためオーバーライドして無効化する
    def destroy(self, request, *args, **kwargs):
        # レスポンスメッセージを作成
        response = {'message': 'DELETE method is not allowed'}
        # レスポンスメッセージとBADリクエストを返す
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        # レスポンスメッセージを作成
        response = {'message': 'PATCH method is not allowed'}
        # レスポンスメッセージとBADリクエストを返す
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def destroy(self, request, *args, **kwargs):
        # レスポンスメッセージを作成
        response = {'message': 'DELETE method is not allowed'}
        # レスポンスメッセージとBADリクエストを返す
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        response = {'message': 'UPDATE method is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        # レスポンスメッセージを作成
        response = {'message': 'PATCH method is not allowed'}
        # レスポンスメッセージとBADリクエストを返す
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    # オーナーでないタスクに関して編集できないようなパーミッションを定義する
    # apiアプリのcustompermissions.pyに記述していくよ
    # その後 permission_classes に定義したパーミッションを割り当てる
    permission_classes = (permissions.IsAuthenticated, custompermissions.OwnerPermission,)

    # タスク作成者がownerにデフォルトで割り当てられるようにする
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # タスクはpertial_updateを使わないためBADリクエストを返すようにする
    def partial_update(self, request, *args, **kwargs):
        response = "PATCH method is not allowed"
        return Response(response, status=status.HTTP_400_BAD_REQUEST)