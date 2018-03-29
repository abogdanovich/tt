# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Preset'
        db.create_table(u'projects_preset', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('challenge', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('service', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True)),
            ('industry', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True)),
            ('solution', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
        ))
        db.send_create_signal(u'projects', ['Preset'])

        # Adding unique constraint on 'Preset', fields ['title']
        db.create_unique(u'projects_preset', ['title'])

        # Adding model 'PresetRequirement'
        db.create_table(u'projects_presetrequirement', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('preset', self.gf('django.db.models.fields.related.ForeignKey')(related_name='requirements', null=True, to=orm['projects.Preset'])),
            ('skill', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='presets', null=True, to=orm['cv.Skill'])),
            ('desc', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'projects', ['PresetRequirement'])

        # Adding unique constraint on 'PresetRequirement', fields ['preset', 'skill']
        db.create_unique(u'projects_presetrequirement', ['preset_id', 'skill_id'])

        # Adding model 'Project'
        db.create_table(u'projects_project', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('challenge', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='projects', to=orm['customers.Customer'])),
            ('benefits', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('feedback', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('service', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True)),
            ('industry', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True)),
            ('solution', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('dev_time', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('date_start', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('date_finish', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('pause', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('preset', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='projects', null=True, blank=True, to=orm['projects.Preset'])),
        ))
        db.send_create_signal(u'projects', ['Project'])

        # Adding model 'Screenshot'
        db.create_table(u'projects_screenshot', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='screenshots', to=orm['projects.Project'])),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('desc', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
        ))
        db.send_create_signal(u'projects', ['Screenshot'])

        # Adding model 'WorkGroup'
        db.create_table(u'projects_workgroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='wg', to=orm['projects.Project'])),
            ('cv', self.gf('django.db.models.fields.related.ForeignKey')(related_name='wg', to=orm['cv.CV'])),
            ('role', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('desc', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('date_start', self.gf('django.db.models.fields.DateField')()),
            ('date_finish', self.gf('django.db.models.fields.DateField')(default=None, null=True, blank=True)),
        ))
        db.send_create_signal(u'projects', ['WorkGroup'])

        # Adding unique constraint on 'WorkGroup', fields ['project', 'cv']
        db.create_unique(u'projects_workgroup', ['project_id', 'cv_id'])

        # Adding model 'ProjectRequirement'
        db.create_table(u'projects_projectrequirement', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='requirements', null=True, to=orm['projects.Project'])),
            ('skill', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='projects', null=True, to=orm['cv.Skill'])),
            ('desc', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'projects', ['ProjectRequirement'])

        # Adding unique constraint on 'ProjectRequirement', fields ['project', 'skill']
        db.create_unique(u'projects_projectrequirement', ['project_id', 'skill_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'ProjectRequirement', fields ['project', 'skill']
        db.delete_unique(u'projects_projectrequirement', ['project_id', 'skill_id'])

        # Removing unique constraint on 'WorkGroup', fields ['project', 'cv']
        db.delete_unique(u'projects_workgroup', ['project_id', 'cv_id'])

        # Removing unique constraint on 'PresetRequirement', fields ['preset', 'skill']
        db.delete_unique(u'projects_presetrequirement', ['preset_id', 'skill_id'])

        # Removing unique constraint on 'Preset', fields ['title']
        db.delete_unique(u'projects_preset', ['title'])

        # Deleting model 'Preset'
        db.delete_table(u'projects_preset')

        # Deleting model 'PresetRequirement'
        db.delete_table(u'projects_presetrequirement')

        # Deleting model 'Project'
        db.delete_table(u'projects_project')

        # Deleting model 'Screenshot'
        db.delete_table(u'projects_screenshot')

        # Deleting model 'WorkGroup'
        db.delete_table(u'projects_workgroup')

        # Deleting model 'ProjectRequirement'
        db.delete_table(u'projects_projectrequirement')


    models = {
        u'customers.customer': {
            'Meta': {'unique_together': "(('name',),)", 'object_name': 'Customer'},
            'address': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'contact': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'desc': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'phone': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'})
        },
        u'cv.cv': {
            'Meta': {'unique_together': "(('login',),)", 'object_name': 'CV'},
            'edit_fl': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'edit_skills': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'fired': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'login': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'position': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'cvs'", 'null': 'True', 'to': u"orm['cv.Position']"}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['timecard.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'cv.position': {
            'Meta': {'unique_together': "(('name',),)", 'object_name': 'Position'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_projects': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'permissions': ('django.db.models.fields.CharField', [], {'default': "'0000000000000000000000000000000000000000000000000000000'", 'max_length': '55'})
        },
        u'cv.skill': {
            'Meta': {'unique_together': "(('name',),)", 'object_name': 'Skill'},
            'desc': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'on_main': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'projects.preset': {
            'Meta': {'unique_together': "(('title',),)", 'object_name': 'Preset'},
            'challenge': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industry': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'service': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'solution': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'projects.presetrequirement': {
            'Meta': {'unique_together': "(('preset', 'skill'),)", 'object_name': 'PresetRequirement'},
            'desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'preset': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'requirements'", 'null': 'True', 'to': u"orm['projects.Preset']"}),
            'skill': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'presets'", 'null': 'True', 'to': u"orm['cv.Skill']"})
        },
        u'projects.project': {
            'Meta': {'object_name': 'Project'},
            'benefits': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'challenge': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'projects'", 'to': u"orm['customers.Customer']"}),
            'date_finish': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_start': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'dev_time': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'feedback': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industry': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'pause': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'preset': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'projects'", 'null': 'True', 'blank': 'True', 'to': u"orm['projects.Preset']"}),
            'service': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'solution': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'projects.projectrequirement': {
            'Meta': {'unique_together': "(('project', 'skill'),)", 'object_name': 'ProjectRequirement'},
            'desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'requirements'", 'null': 'True', 'to': u"orm['projects.Project']"}),
            'skill': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'projects'", 'null': 'True', 'to': u"orm['cv.Skill']"})
        },
        u'projects.screenshot': {
            'Meta': {'object_name': 'Screenshot'},
            'desc': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'screenshots'", 'to': u"orm['projects.Project']"})
        },
        u'projects.workgroup': {
            'Meta': {'unique_together': "(('project', 'cv'),)", 'object_name': 'WorkGroup'},
            'cv': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'wg'", 'to': u"orm['cv.CV']"}),
            'date_finish': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'date_start': ('django.db.models.fields.DateField', [], {}),
            'desc': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'wg'", 'to': u"orm['projects.Project']"}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'timecard.user': {
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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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