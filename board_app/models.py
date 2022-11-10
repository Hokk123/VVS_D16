from ckeditor_uploader.fields import RichTextUploadingField
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Category(models.Model):
    categoryName = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f'{self.categoryName}'


class Post(models.Model):
    authorUser = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    content = RichTextUploadingField()
    upload = models.FileField(
        upload_to='uploads/%Y/%m/%d/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['mp4'])],
    )
    creationDate = models.DateTimeField(auto_now_add=True)
    postCategory = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        """Функция перенаправления пользователя после добавления или изменения данных в бд"""
        return reverse('post_detail', kwargs={'pk': self.id})


class UserReply(models.Model):
    userReply = models.ForeignKey(User, on_delete=models.CASCADE)
    postReply = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    creationDate = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.text}'
