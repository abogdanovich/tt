# -*- coding: utf-8 -*-
__author__ = 'ABKorotky'
__email__ = ['akorotky@minsk.ximxim.com', 'aleksandr.korotky@ximad.com']


from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from timecard import utils
from erp.utils import ttUser, get_cv, check_login, check_permission

from models import *
from forms import *


@check_login
def list_vf(request):
    cv = get_cv(request)
    if not check_permission(cv, perm_index=2): # view customer data
        messages.error(request, "Access denied")
        return redirect("erp_home")
    return render_to_response(
        "customers/customers.html",
        {
            'cv': cv,
            'nav': "customer",
            'customers': Customer.objects.all(),},
        RequestContext(request))


@check_login
def view_vf(request, c_id=None):
    return render_to_response(
        "customers/customers.html",
        {
            'cv': get_cv(request),
            'nav': "customer",
        },
        RequestContext(request))


@check_login
def mod_vf(request, c_id=None, op=""):
    cv = get_cv(request)
    if not check_permission(cv, perm_index=3): # manage customer data
        messages.error(request, "Access denied")
        return redirect("erp_home")
    stage = request.REQUEST.get('stage', None)
    if op == 'add':
        if stage == 'validate':
            c_mform = CustomerMForm(request.POST)
            if c_mform.is_valid():
                c_mform.save()
                messages.success(request, 'Customer data saved successfully.')
                return redirect("erp_customers")
            else:
                messages.error(request, 'Customer data didn`t save. You have some errors.')
        else:
            c_mform = CustomerMForm()
    else: # op == 'mod' or 'del'
        if c_id:
            customer = Customer.objects.get(id=int(c_id))
            if stage == 'validate':
                try:
                    c_mform = CustomerMForm(request.POST, instance=customer)
                    if c_mform.is_valid():
                        c_mform.save()
                        messages.success(request, 'Customer data saved successfully.')
                        return redirect("erp_customers")
                    else:
                        messages.error(request, 'Customer data didn`t save. You have some errors.')
                except Customer.DoesNotExist, Customer.MultipleObjectsReturned:
                    messages.error(request, 'Customer was not found.')
                    redirect("customers")
            else:
                c_mform = CustomerMForm(instance=customer)
        else:
            messages.error(request, 'Bad request')
            return redirect("customers")
    return render_to_response(
        "customers/customer_mod.html",
        {
            'cv': get_cv(request),
            'nav': "customer",
            'op': op,
            'c_mform': c_mform},
        RequestContext(request))
