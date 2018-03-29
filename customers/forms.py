# -*- coding: utf-8 -*-
__author__ = 'ABKorotky'
__email__ = ['akorotky@minsk.ximxim.com', 'aleksandr.korotky@ximad.com']


from datetime import date
from django.forms import Form, ModelForm
from django.forms import IntegerField, BooleanField, CharField, ModelChoiceField
from django.forms import TextInput, Select, HiddenInput, Textarea
from django.forms.models import formset_factory, modelformset_factory, inlineformset_factory

from models import Customer


class CustomerMForm(ModelForm):

    class Meta:
        model = Customer


CustomerMFormset = modelformset_factory(Customer, CustomerMForm, extra=0, can_delete=True)