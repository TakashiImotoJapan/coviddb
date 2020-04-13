from django.db import models
import datetime
from coviddb.util.util import is_int
import numpy as np

class InfectedPerson(models.Model):
    id = models.AutoField(primary_key=True)
    state = models.CharField(default='', max_length=16)
    pat_id = models.IntegerField()
    city_no = models.CharField(default='', max_length=16, null=True)
    announce_date = models.CharField(default='', max_length=10, null=True)
    infected_date = models.CharField(default='', max_length=10, null=True)
    living_state = models.CharField(default='', max_length=24, null=True)
    living_city = models.CharField(default='', max_length=24, null=True)
    age = models.IntegerField(default=999, null=True)
    sex = models.IntegerField(default=2, null=True)
    status = models.CharField(default='', max_length=24, null=True)
    symptoms = models.CharField(default='', max_length=128, null=True)
    occupation = models.CharField(default='', max_length=24, null=True)
    close_contact = models.CharField(default='', max_length=64, null=True)
    rel_close_contact = models.CharField(default='', max_length=256, null=True)
    travel_history = models.IntegerField(null=True)
    travel_destination = models.CharField(default='', max_length=128, null=True)
    remarks = models.CharField(default='', max_length=2048, null=True)
    cluster_location = models.CharField(default='', max_length=128, null=True)
    cluster_name = models.CharField(default='', max_length=256, null=True)
    discharge = models.IntegerField(null=True)
    death = models.IntegerField(null=True)
    death_date = models.CharField(default='', max_length=10, null=True)
    full_presentation = models.CharField(default='', max_length=8096, null=True)

    def createDateStr(self, val):
        if type(val) == datetime.datetime:
            return val.strftime('%Y/%m/%d')
        elif type(val) == str:
            return val.replace('-', '/')
        else:
            return ''

    def setAge(self, val):
        val = val.strip("代")
        if val.isdecimal():
            self.age = int(val)
        else:
            self.age = 999

    def setCloseContact(self, val):
        if is_int(val) or type(val) == int:
            self.close_contact += "%s-%s " % (self.state, val)
        else:
            self.close_contact += "%s " % (val)

    def setSexStr(self, val):
        if(val != None):
            if val.find('男') >= 0:
                self.sex = 0
            elif val.find('女') >= 0:
                self.sex = 1
            else:
                self.sex = 2

    def setStatus(self, val):
        if '軽' in val or '中' in val :
            self.status = '軽症'
        elif '無症状' in val:
            self.status = '無症状'
        elif '重' in val:
            self.status = '重症'

    def to_csv(self):
        csv = []

        for f in self._meta.get_fields():
            val = str(getattr(self, f.name))
            val = '' if val == 'None' or val == 'nan' or val == '不明' else val
            if f.name != 'id':
                csv.append(val)

        return ','.join(csv)


    def __setattr__(self, attrname, val):
        super(InfectedPerson, self).__setattr__(attrname, val)


    def __getattr__(self, attrname):
        return super(InfectedPerson, self).__getattr__(attrname)

#    def __str__(self):
#        return "%s-%s" % (self.state, str(self.pat_id))

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
    plus = models.IntegerField(null=True)
    discharge_per = models.FloatField(null=True)
    death = models.IntegerField(null=True)
    state_id = models.IntegerField(null=True)
    date = models.CharField(max_length=16, null=True)

    def __str__(self):
        return self.state
