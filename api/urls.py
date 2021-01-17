from django.urls import path, include
from rest_framework import routers
from .views import TaskViewSet, CategoryViewSet, CreateUserView, ListUserView, LoginUserView, ProfileViewSet


# viewsでmodelViewSetsで定義したものはrouternでviewとURLを紐づけていく
# genericでメゾットを定義したviewはurlpatternsに記述する
# 後ほどviewで作っていくmodelrouterとviewのnameとの紐付けをこのdefaultRouterで実施する
router = routers.DefaultRouter()
# router.register('引数１=>urlName', viewSetName) でviewSetを登録していく
router.register('category', CategoryViewSet)
router.register('tasks', TaskViewSet)
router.register('profile', ProfileViewSet)


urlpatterns = [
    # apiアプリにアクセスがあるたびにrouterを参照するようになる
    path('', include(router.urls)),

    path('create/', CreateUserView.as_view(), name="create"),
    path('users/', ListUserView.as_view(), name="users"),
    path('loginuser/', LoginUserView.as_view(), name="loginuser"),
]