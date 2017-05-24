from django.db import models
from django.utils import timezone


class User(models.Model):
    id = models.AutoField(primary_key=True)
    login = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    created_date = models.DateTimeField(
            default=timezone.now)

    def __str__(self):
        return self.login

    def publish(self):
        self.published_date = timezone.now()
        self.save()


class Site(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    viewId = models.IntegerField()
    url = models.CharField(max_length=64, default='')

    def __str__(self):
        return self.url

    def publish(self):
        self.save()


class Lost_site(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    site = models.ForeignKey(Site)

    def __str__(self):
        return str(self.id)

    def publish(self):
        self.save()


class Metric(models.Model):
    value = models.CharField(max_length=32)
    ru = models.CharField(max_length=48)
    en = models.CharField(max_length=48)

    def __str__(self):
        return self.value

    def publish(self):
        self.save()


class Chart(models.Model):
    site = models.ForeignKey(Site)
    metric = models.ForeignKey(Metric)
    startDate = models.CharField(max_length=16)
    endDate = models.CharField(max_length=16)
    width = models.IntegerField(default=1280)
    height = models.IntegerField(default=480)

    def __str__(self):
        return self.site.__str__()+' '+self.metric.value

    def publish(self):
        self.save()