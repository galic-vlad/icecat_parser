#-*- coding: UTF-8 -*-
from django.db import models


class MeasureSign(models.Model):
    measure = models.ForeignKey('Measure')
    language = models.ForeignKey('Language')
    value = models.CharField(max_length=255, default='')

    def __unicode__(self):
        return unicode(self.id)

    class Meta:
        app_label = 'iceparser'