from django.db import models
from django.contrib.auth.models import User

# バリーデート時に負の数を受け付けないようにするためのパッケージpakke-ji
from django.core.validators import MinValueValidator

# PKが連番だとセキュリティ上よくないためUniversal Unique IDという128bitの一意な値を作ってくれるパッケージを使うtukau
import uuid

def upload_avatar_path(instance, filename):
    # 拡張子を抽出
    ext = filename.split('.')[-1]
    return '/'.join(['avatars', str(instance.user_profile.id)+ str(".")+ str(ext)])

class Profile(models.Model):
    user_profile = models.OneToOneField(
        User, related_name='user_profile',
        on_delete=models.CASCADE
    )
    img = models.ImageField(blank=True, null=True, upload_to=upload_avatar_path)

    def __str__(self):
        return self.user_profile.username


class Category(models.Model):
    item = models.CharField(max_length=100)

    def __str__(self):
        return self.item

class Task(models.Model):

    STATUS = (
        ('1', 'Not started'),
        ('2', 'On going'),
        ('3', 'Done'),
    )

    # uuidで一意なIDを割り当てる、primary_keyはTrue, 編集は不可fuka
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    task = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    criteria = models.CharField(max_length=100)
    status = models.CharField(max_length=40, choices=STATUS, default='1')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # マイナスの数字を受け取らない用意にするためミニマムバリューを0にする
    estimate = models.IntegerField(validators=[MinValueValidator(0)])
    owner = models.ForeignKey(User, related_name="owner", on_delete=models.CASCADE)
    responsible = models.ForeignKey(User, related_name="rasponsible", on_delete=models.CASCADE, null=True)
    # auto_now_add: インスタンスが作成されたとき　auto_now: インスタンスが更新されるたびに
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.task