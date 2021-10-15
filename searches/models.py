from django.db import models
from accounts.models import Account


class Search(models.Model):
    search_text = models.TextField()
    search_type = models.CharField(max_length=100)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return self.search_text