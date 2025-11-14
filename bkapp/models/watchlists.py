from django.db import models
from .base import BaseModel


class Watchlist(BaseModel):
    class Meta:
        db_table = 'watchlists'

    user_id = models.IntegerField()
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def to_dict(self):
        """转换为字典"""
        data = super().to_dict()
        data.update({
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description
        })
        return data

    def __str__(self):
        return f'<Watchlist {self.user_id}:{self.name}>'