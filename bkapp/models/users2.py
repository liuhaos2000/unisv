from django.contrib.auth.models import AbstractUser
from django.db import models

class User2(AbstractUser):
    phone = models.CharField(max_length=30, null=True, blank=True)
    is_vip = models.BooleanField(default=False)

    def to_dict(self):
        """返回字典，不包含密碼"""
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'phone': self.phone,
            'is_vip': self.is_vip,
        }
        return data

    def __str__(self):
        return f'<User {self.username}>'
