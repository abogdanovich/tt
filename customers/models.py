# -*- coding: utf-8 -*-
__author__ = 'ABKorotky'
__email__ = ['akorotky@minsk.ximxim.com', 'aleksandr.korotky@ximad.com']


from datetime import date
from django.db import models

from cv.models import CV, Skill


class Customer(models.Model):
    """
    customer info
    """
    name = models.CharField("Customer", max_length=200)
    country = models.CharField("Country", max_length=100, blank=True, default="")
    address = models.TextField("Address", blank=True, default="")
    contact = models.CharField("Contact Person", max_length=100, blank=True, default="")
    phone = models.CharField("Phone number(s)", max_length=100, blank=True, default="")
    email = models.EmailField("E-Mail", max_length=50, blank=True, default="")
    desc = models.TextField("Other Information", blank=True, default="")

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
        unique_together = ('name', )

    def __unicode__(self):
        return self.name