from django.db import models
from accounts.models import Account, Skill
from applications.models import Application


class WorkDescription(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text


class Reward(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text


class Project(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField()
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    type = models.CharField(max_length=30)
    requirements = models.ManyToManyField(Skill)
    created_at = models.DateTimeField(auto_now_add=True)
    place = models.CharField(max_length=500)
    payment = models.IntegerField()
    work_description = models.ManyToManyField(WorkDescription)
    reward = models.ManyToManyField(Reward)
    target = models.IntegerField()
    completed = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    positions = models.IntegerField(default=0)
    views = models.ManyToManyField(Account, related_name='views')
    applications = models.ManyToManyField(Application)

    def __str__(self):
        return self.title