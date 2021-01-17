

# フロントエンドにどのようなJSON形式を渡すのか定義するのがシリアライザー
# シリアライザーは基本的にモデル１つ１つに対して作っていく
from rest_framework import serializers
from .models import Task, Category, Profile
from django.contrib.auth.models import User

# Userモデルに対するUserシリアライザーを書いていく
# シリアライザーはclass Metaに書く
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        # 特定のパラメーターに対してさらにオプションを付与できる
        # passwordに対して読み取れないように write_only を true に
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    # passwordをハッシュ化してDBに保存するためcreateメゾットをオーバーライドする
    def create(self, validated_data):
        # create_userに **validated_data を渡すことでハッシュ化したパスワードをuserに返せる
        user = User.objects.create_user(**validated_data)
        return user

class ProfileSirializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user_profile', 'img']
        # sepalate operation in Create and Read
        extra_keargs = {"user_profile": {"read_only": True}}

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'item']

class TaskSerializer(serializers.ModelSerializer):
    # 紐づいてるモデルの値を取得して予め変数に代入しておく
    category_item = serializers.ReadOnlyField(source="category.item", read_only=True)
    owner_username = serializers.ReadOnlyField(source="user.username", read_only=True)
    responsible_username = serializers.ReadOnlyField(source="responsible.username", read_only=True)
    status_name = serializers.CharField(source="get_status_display", read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'task', 'description', 'criteria', 'status', 'status_name',
                  'category', 'category_item', 'estimate', 'responsible', 'responsible_username',
                  'owner', 'owner_username', 'created_at', 'updated_at',
                  ]
        extra_kwargs = {'owner': {'read_only': True}}