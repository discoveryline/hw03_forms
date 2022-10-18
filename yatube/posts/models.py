from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Название группы',
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Ключ',
        help_text='Ключ для группы в адресной строке',
    )
    description = models.TextField(
        verbose_name='Описание',
    )

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(
        verbose_name='Текст поста',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )
    author = models.ForeignKey(
        User,
        related_name='posts',
        verbose_name='Автор публикации',
        on_delete=models.CASCADE,
    )
    group = models.ForeignKey(
        Group,
        related_name='posts',
        verbose_name='Группа',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.text
