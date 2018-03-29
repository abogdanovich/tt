# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'ProjectVersion'
        db.delete_table('projects_projectversion')

        # Adding field 'Project.challenge'
        db.add_column('projects_project', 'challenge',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'Project.benefits'
        db.add_column('projects_project', 'benefits',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'Project.feedback'
        db.add_column('projects_project', 'feedback',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'Project.service'
        db.add_column('projects_project', 'service',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True),
                      keep_default=False)

        # Adding field 'Project.industry'
        db.add_column('projects_project', 'industry',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True),
                      keep_default=False)

        # Adding field 'Project.solution'
        db.add_column('projects_project', 'solution',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'Project.tools'
        db.add_column('projects_project', 'tools',
                      self.gf('django.db.models.fields.TextField')(default='', max_length=255, blank=True),
                      keep_default=False)

        # Adding field 'Project.servers'
        db.add_column('projects_project', 'servers',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Project.databases'
        db.add_column('projects_project', 'databases',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'Project.testing'
        db.add_column('projects_project', 'testing',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'Project.vcs'
        db.add_column('projects_project', 'vcs',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'ProjectVersion'
        db.create_table('projects_projectversion', (
            ('feedback', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('testing', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('servers', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('date_create', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=datetime.datetime(2013, 4, 10, 0, 0), blank=True)),
            ('vcs', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('tools', self.gf('django.db.models.fields.TextField')(default='', max_length=255, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('benefits', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('service', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True)),
            ('industry', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True)),
            ('solution', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='versions', to=orm['projects.Project'])),
            ('databases', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('challenge', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
        ))
        db.send_create_signal('projects', ['ProjectVersion'])

        # Deleting field 'Project.challenge'
        db.delete_column('projects_project', 'challenge')

        # Deleting field 'Project.benefits'
        db.delete_column('projects_project', 'benefits')

        # Deleting field 'Project.feedback'
        db.delete_column('projects_project', 'feedback')

        # Deleting field 'Project.service'
        db.delete_column('projects_project', 'service')

        # Deleting field 'Project.industry'
        db.delete_column('projects_project', 'industry')

        # Deleting field 'Project.solution'
        db.delete_column('projects_project', 'solution')

        # Deleting field 'Project.tools'
        db.delete_column('projects_project', 'tools')

        # Deleting field 'Project.servers'
        db.delete_column('projects_project', 'servers')

        # Deleting field 'Project.databases'
        db.delete_column('projects_project', 'databases')

        # Deleting field 'Project.testing'
        db.delete_column('projects_project', 'testing')

        # Deleting field 'Project.vcs'
        db.delete_column('projects_project', 'vcs')


    models = {
        'cv.cv': {
            'Meta': {'object_name': 'CV'},
            'edit_fl': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'edit_skills': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'position': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cv.Position']", 'null': 'True', 'blank': 'True'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'cv'", 'unique': 'True', 'null': 'True', 'to': "orm['timecard.User']"})
        },
        'cv.position': {
            'Meta': {'unique_together': "(('name',),)", 'object_name': 'Position'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
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
            'challenge': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'projects'", 'to': "orm['projects.Customer']"}),
            'databases': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'date_finish': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_start': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'dev_time': ('django.db.models.fields.IntegerField', [], {}),
            'feedback': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industry': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'is_pause': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'servers': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'service': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'solution': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'testing': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'tools': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'vcs': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'})
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
            'cv': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'wg'", 'to': "orm['cv.CV']"}),
            'date_finish': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'date_start': ('django.db.models.fields.DateField', [], {}),
            'desc': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'wg'", 'to': "orm['projects.Project']"}),
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