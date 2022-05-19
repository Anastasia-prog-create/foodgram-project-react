from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя."""
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name',
    )
    
    email = models.EmailField(max_length=255, unique=True)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return str(f'{self.username} {self.email}')


class Subscribe(models.Model):
    """Модель подписки."""
    user = models.ForeignKey(
        User,
        related_name='user',
        on_delete=models.CASCADE,
    )
    subscriber = models.ForeignKey(
        User,
        related_name='subscriber',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'subscriber'],
                name='unique subscribe'
            ),
        ]

    def __str__(self):
        return f'{self.user.username} -> {self.subscriber.username}'
