from rest_framework.permissions import BasePermission

# Проверка прав пользователя на то или иное действие
from backend.models import Profile


class IsOwnerOrReadOnly(BasePermission):

    # has_object_permission - метод для работы с конкретным объектом
    def has_object_permission(self, request, view, obj):
        # если запрос на просмотр - всегда возвращаем true
        # нужно для возможности просмотра любого отчета
        if request.method == 'GET':
            return True

        # возвращаем false или true в зависимости от владельца объекта
        return request.user == obj.user


class IsOwnerOrReadOnlyProfile(BasePermission):

    # has_object_permission - метод для работы с конкретным объектом
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user