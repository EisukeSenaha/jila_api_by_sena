from rest_framework import permissions

# カスタムのパーミッションとしてOwnerPermissionsを作成していく
class OwnerPermission(permissions.BasePermission):

    # has_object_permissionをオーバーライドする
    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS とはGETなどOBJを書き換えることがないメゾットをさす
        # safe_methodならTrueを返す＝＞ permissionを許可すると等価
        if request.method in permissions.SAFE_METHODS:
            return True
        # ownerとログインユーザーが同じならtrueを返す
        return obj.owner.id == request.user.id

        # このパーミッションを使ってTaskViewSetsを上書きする
        # views.pyへ


