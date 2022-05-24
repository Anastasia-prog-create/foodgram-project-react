from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from djoser import views
from rest_framework import filters, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.serializers import (PasswordSerializer, SubscribeSerializer,
                             SubscribesListSerializer, UserCreateSerializer,
                             UserSerializer)
                             
from .models import Subscribe, User
from .permissions import AdminOrUserOrReadOnly
from backend.pagination import FoodgramPagination


class CustomUserViewSet(views.UserViewSet):
    """ViewSet для модели User."""
    queryset = User.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username', )
    permission_classes = (AdminOrUserOrReadOnly, )

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    @action(detail=False, methods=['post'],
            permission_classes=AdminOrUserOrReadOnly)
    def set_password(self, request, pk=None):
        user = self.request.user
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'status': 'password set'})
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, permission_classes=(permissions.IsAuthenticated,),
            pagination_class=FoodgramPagination,)
    def subscriptions(self, request):
        queryset = User.objects.filter(
                user__subscriber=request.user).annotate(
                    recipes_count=Count(
                        'author', filter=Q(user__subscriber=request.user)
                        )
                    )
        serializer = SubscribesListSerializer(
            queryset,
            many=True,
            context={
                'request': request,
                'format': self.format_kwarg,
                'view': self
                }
            )
        return Response(serializer.data)

    @action(detail=True, methods=['post', 'delete'],)
    def subscribe(self, request, id):
        if request.method == 'POST':
            if int(id) == request.user.id:
                return Response(
                    {'status': 'Подписка на себя невозможна.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if Subscribe.objects.filter(
                user=get_object_or_404(User, id=id),
                subscriber=self.request.user
            ).exists():
                return Response(
                    {'status': 'Такая подписка уже существует.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            subscribe = Subscribe.objects.create(
                user=get_object_or_404(User, id=id),
                subscriber=self.request.user
            )
            serializer = SubscribeSerializer(subscribe)
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )

        if request.method == 'DELETE':
            subscribe = get_object_or_404(
                Subscribe,
                user_id=id,
                subscriber=self.request.user
            )
            subscribe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'status': 'Такая подписка не существует.'},
            status=status.HTTP_400_BAD_REQUEST
        )
