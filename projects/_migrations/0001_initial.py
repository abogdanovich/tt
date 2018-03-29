# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Customer'
        db.create_table('projects_customer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('country', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True)),
            ('address', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('contact', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(default='', max_length=50, blank=True)),
            ('desc', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
        ))
        db.send_create_signal('projects', ['Customer'])

        # Adding unique constraint on 'Customer', fields ['name']
        db.create_unique('projects_customer', ['name'])

        # Adding model 'Project'
        db.create_table('projects_project', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('code', self.gf('django.db.models.fields.CharField')(default='', max_length=50, blank=True)),
            ('challenge', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='projects', to=orm['projects.Customer'])),
            ('benefits', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('service', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('dev_time', self.gf('django.db.models.fields.IntegerField')()),
            ('date_start', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('date_finish', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
        ))
        db.send_create_signal('projects', ['Project'])

        # Adding model 'Screenshot'
        db.create_table('projects_screenshot', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='screenshots', to=orm['projects.Project'])),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('desc', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
        ))
        db.send_create_signal('projects', ['Screenshot'])

        # Adding model 'WorkGroup'
        db.create_table('projects_workgroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='employees', to=orm['projects.Project'])),
            ('cv', self.gf('django.db.models.fields.related.ForeignKey')(related_name='projects', to=orm['cv.CV'])),
            ('role', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('desc', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('date_start', self.gf('django.db.models.fields.DateField')()),
            ('date_finish', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('projects', ['WorkGroup'])

        # Adding unique constraint on 'WorkGroup', fields ['project', 'cv']
        db.create_unique('projects_workgroup', ['project_id', 'cv_id'])

        # Adding model 'ProjectHistory'
        db.create_table('projects_projecthistory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('wg', self.gf('django.db.models.fields.related.ForeignKey')(related_name='history', to=orm['projects.WorkGroup'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('desc', self.gf('django.db.models.fields.TextField')()),
            ('hours', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
        ))
        db.send_create_signal('projects', ['ProjectHistory'])


    def backwards(self, orm):
        # Removing unique constraint on 'WorkGroup', fields ['project', 'cv']
        db.delete_unique('projects_workgroup', ['project_id', 'cv_id'])

        # Removing unique constraint on 'Customer', fields ['name']
        db.delete_unique('projects_customer', ['name'])

        # Deleting model 'Customer'
        db.delete_table('projects_customer')

        # Deleting model 'Project'
        db.delete_table('projects_project')

        # Deleting model 'Screenshot'
        db.delete_table('projects_screenshot')

        # Deleting model 'WorkGroup'
        db.delete_table('projects_workgroup')

        # Deleting model 'ProjectHistory'
        db.delete_table('projects_projecthistory')


    models = {
        'cv.cv': {
            'Meta': {'object_name': 'CV'},
            'edit_fl': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'edit_skills': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'position': ('django.db.models.fields.CharField', [], {'default': "'no data...'", 'max_length': '100'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'cv'", 'null': 'True', 'default': 'None', 'to': "orm['timecard.User']", 'blank': 'True', 'unique': 'True'})
        },
        'projects.customer': {
            'Meta': {'unique_together': "(('name',),)", 'object_name': 'Customer'},
            'address': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'contact': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'desc': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'phone': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'})
        },
        'projects.project': {
            'Meta': {'object_name': 'Project'},
            'benefits': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'challenge': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'projects'", 'to': "orm['projects.Customer']"}),
            'date_finish': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_start': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'dev_time': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'service': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'state': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'projects.projecthistory': {
            'Meta': {'object_name': 'ProjectHistory'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'desc': ('django.db.models.fields.TextField', [], {}),
            'hours': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'wg': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'history'", 'to': "orm['projects.WorkGroup']"})
        },
        'projects.screenshot': {
            'Meta': {'object_name': 'Screenshot'},
            'desc': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'screenshots'", 'to': "orm['projects.Project']"})
        },
        'projects.workgroup': {
            'Meta': {'unique_together': "(('project', 'cv'),)", 'object_name': 'WorkGroup'},
            'cv': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'projects'", 'to': "orm['cv.CV']"}),
            'date_finish': ('django.db.models.fields.DateField', [], {}),
            'date_start': ('django.db.models.fields.DateField', [], {}),
            'desc': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'employees'", 'to': "orm['projects.Project']"}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'timecard.user': {
            'Meta': {'object_name': 'User'},
            'accessLevel': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '1'}),
            'avator': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'counter01': ('django.db.models.fields.IntegerField', [], {}),
            'dep': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'email': ('django.db.models.fields.EmailField', [], {'default': "'@minsk.ximxim.com'", 'max_length': '150'}),
            'fb': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': '1', 'max_length': '2'}),
            'group': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'hb': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'login': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'office': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'profession': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'skype': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'twitter': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'ua': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'voted': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['projects']
