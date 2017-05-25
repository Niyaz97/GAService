from django.db import models
from django.utils import timezone


class Lost_site(models.Model):
    list = models.CharField(max_length = 160)
    viewId = models.BigIntegerField()


    def __str__(self):
        return str(self.id)

    def publish(self):
        self.save()


class Metric(models.Model):
    value = models.CharField(max_length = 32)
    ru = models.CharField(max_length = 48)
    en = models.CharField(max_length = 48)

    def __str__(self):
        return self.value

    def publish(self):
        self.save()


class Chart(models.Model):
    viewId = models.BigIntegerField()
    metric = models.ForeignKey(Metric)
    startDate = models.CharField(max_length=16)
    endDate = models.CharField(max_length=16)
    width = models.IntegerField(default = 1280)
    height = models.IntegerField(default = 480)
    max_count = models.IntegerField(default = 16)
    numb = models.IntegerField(default=1)

    def __str__(self):
        return str(self.viewId)+' '+self.metric.value

    def publish(self):
        self.save()

    class Meta:
        ordering = ["numb"]