from django.db import models

class State(models.Model):
    id = models.IntegerField(primary_key=True)
    jp = models.CharField(max_length=100)
    kana = models.CharField(max_length=100)
    romam = models.CharField(max_length=100)
    disp = models.IntegerField()
    color = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.romam

class JapanInfectedNumber(models.Model):

    state = models.CharField(max_length=128)
    positive = models.IntegerField(null=True)
    hospitalization = models.IntegerField(null=True)
    discharge = models.IntegerField(null=True)
    death = models.IntegerField(null=True)
    state_id = models.IntegerField(null=True)
    date = models.CharField(max_length=16, null=True)

    def __str__(self):
        return self.state
