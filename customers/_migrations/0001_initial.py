# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Customer'
        db.create_table('customers_customer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('country', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True)),
            ('address', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('contact', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(default='', max_length=50, blank=True)),
            ('desc', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
        ))
        db.send_create_signal('customers', ['Customer'])

        # Adding unique constraint on 'Customer', fields ['name']
        db.create_unique('customers_customer', ['name'])


    def backwards(self, orm):
        # Removing unique constraint on 'Customer', fields ['name']
        db.delete_unique('customers_customer', ['name'])

        # Deleting model 'Customer'
        db.delete_table('customers_customer')


    models = {
        'customers.customer': {
            'Meta': {'unique_together': "(('name',),)", 'object_name': 'Customer'},
            'address': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'contact': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'desc': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'phone': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'})
        }
    }

    complete_apps = ['customers']