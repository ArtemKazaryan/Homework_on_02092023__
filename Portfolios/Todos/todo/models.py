# from django.db import models
# from django.contrib.auth.models import User


# models.CASCADE - если удалится пользователь, то будут удалены все его задачи
# models.PROTECT - если у пользователя существует хотя бы одна задача, этот флаг не даст
# его(пользователя) удалить
# models.SET_NULL - если удалится пользователь, то указание на пользователя превратится
# в NULL
# models.SET_DEFAULT - то же самое, что и SET_NULL, но вместо изменения на NUll, будет
# происходить изменение на значение по умолчанию

from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    # date_completed = models.DateTimeField(null=True, blank=True)
    # important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    image = models.ImageField(upload_to='todos/images', null=True)
    url = models.CharField(max_length=350, null=True)
    # url = models.URLField(blank=True)
    # file_url = models.CharField(max_length=350, null=True)

    def __str__(self):
        return self.title

# class Todo(models.Model):
#     title = models.CharField(max_length=100)
#     description = models.TextField(blank=True)
#     created = models.DateTimeField(auto_now_add=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
#     url = models.CharField(max_length=100, null=True)
#
#     def __str__(self):
#         return self.title