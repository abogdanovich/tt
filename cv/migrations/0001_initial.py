# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Skill'
        db.create_table(u'cv_skill', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('desc', self.gf('django.db.models.fields.TextField')(default=None, null=True, blank=True)),
            ('on_main', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'cv', ['Skill'])

        # Adding unique constraint on 'Skill', fields ['name']
        db.create_unique(u'cv_skill', ['name'])

        # Adding model 'Position'
        db.create_table(u'cv_position', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('in_projects', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('permissions', self.gf('django.db.models.fields.CharField')(default='0000000000000000000000000000000000000000000000000000000', max_length=55)),
        ))
        db.send_create_signal(u'cv', ['Position'])

        # Adding unique constraint on 'Position', fields ['name']
        db.create_unique(u'cv_position', ['name'])

        # Adding model 'CV'
        db.create_table(u'cv_cv', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('surname', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('position', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='cvs', null=True, to=orm['cv.Position'])),
            ('login', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['timecard.User'], unique=True, null=True, blank=True)),
            ('fired', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('edit_fl', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('edit_skills', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'cv', ['CV'])

        # Adding unique constraint on 'CV', fields ['login']
        db.create_unique(u'cv_cv', ['login'])

        # Adding model 'Contact'
        db.create_table(u'cv_contact', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cv', self.gf('django.db.models.fields.related.ForeignKey')(related_name='contacts', to=orm['cv.CV'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('val', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'cv', ['Contact'])

        # Adding unique constraint on 'Contact', fields ['cv', 'name']
        db.create_unique(u'cv_contact', ['cv_id', 'name'])

        # Adding model 'FL'
        db.create_table(u'cv_fl', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cv', self.gf('django.db.models.fields.related.ForeignKey')(related_name='fl', to=orm['cv.CV'])),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('spoken', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('written', self.gf('django.db.models.fields.SmallIntegerField')()),
        ))
        db.send_create_signal(u'cv', ['FL'])

        # Adding unique constraint on 'FL', fields ['cv', 'language']
        db.create_unique(u'cv_fl', ['cv_id', 'language'])

        # Adding model 'CVSkill'
        db.create_table(u'cv_cvskill', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cv', self.gf('django.db.models.fields.related.ForeignKey')(related_name='skills', null=True, to=orm['cv.CV'])),
            ('skill', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='cvs', null=True, to=orm['cv.Skill'])),
            ('desc', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
        ))
        db.send_create_signal(u'cv', ['CVSkill'])

        # Adding unique constraint on 'CVSkill', fields ['cv', 'skill']
        db.create_unique(u'cv_cvskill', ['cv_id', 'skill_id'])

        # Adding model 'Certificate'
        db.create_table(u'cv_certificate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cv', self.gf('django.db.models.fields.related.ForeignKey')(related_name='certificates', to=orm['cv.CV'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('desc', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'cv', ['Certificate'])

        # Adding unique constraint on 'Certificate', fields ['cv', 'title']
        db.create_unique(u'cv_certificate', ['cv_id', 'title'])

        # Adding model 'PrevProject'
        db.create_table(u'cv_prevproject', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cv', self.gf('django.db.models.fields.related.ForeignKey')(related_name='prev_projects', to=orm['cv.CV'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('challenge', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('role', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('desc', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('date_start', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('date_finish', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'cv', ['PrevProject'])

        # Adding unique constraint on 'PrevProject', fields ['cv', 'title']
        db.create_unique(u'cv_prevproject', ['cv_id', 'title'])

        # Adding model 'PrevScreenshot'
        db.create_table(u'cv_prevscreenshot', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='screenshots', to=orm['cv.PrevProject'])),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('desc', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
        ))
        db.send_create_signal(u'cv', ['PrevScreenshot'])


    def backwards(self, orm):
        # Removing unique constraint on 'PrevProject', fields ['cv', 'title']
        db.delete_unique(u'cv_prevproject', ['cv_id', 'title'])

        # Removing unique constraint on 'Certificate', fields ['cv', 'title']
        db.delete_unique(u'cv_certificate', ['cv_id', 'title'])

        # Removing unique constraint on 'CVSkill', fields ['cv', 'skill']
        db.delete_unique(u'cv_cvskill', ['cv_id', 'skill_id'])

        # Removing unique constraint on 'FL', fields ['cv', 'language']
        db.delete_unique(u'cv_fl', ['cv_id', 'language'])

        # Removing unique constraint on 'Contact', fields ['cv', 'name']
        db.delete_unique(u'cv_contact', ['cv_id', 'name'])

        # Removing unique constraint on 'CV', fields ['login']
        db.delete_unique(u'cv_cv', ['login'])

        # Removing unique constraint on 'Position', fields ['name']
        db.delete_unique(u'cv_position', ['name'])

        # Removing unique constraint on 'Skill', fields ['name']
        db.delete_unique(u'cv_skill', ['name'])

        # Deleting model 'Skill'
        db.delete_table(u'cv_skill')

        # Deleting model 'Position'
        db.delete_table(u'cv_position')

        # Deleting model 'CV'
        db.delete_table(u'cv_cv')

        # Deleting model 'Contact'
        db.delete_table(u'cv_contact')

        # Deleting model 'FL'
        db.delete_table(u'cv_fl')

        # Deleting model 'CVSkill'
        db.delete_table(u'cv_cvskill')

        # Deleting model 'Certificate'
        db.delete_table(u'cv_certificate')

        # Deleting model 'PrevProject'
        db.delete_table(u'cv_prevproject')

        # Deleting model 'PrevScreenshot'
        db.delete_table(u'cv_prevscreenshot')


    models = {
        u'cv.certificate': {
            'Meta': {'unique_together': "(('cv', 'title'),)", 'object_name': 'Certificate'},
            'cv': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'certificates'", 'to': u"orm['cv.CV']"}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'cv.contact': {
            'Meta': {'unique_together': "(('cv', 'name'),)", 'object_name': 'Contact'},
            'cv': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'contacts'", 'to': u"orm['cv.CV']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'val': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
        u'cv.cvskill': {
            'Meta': {'unique_together': "(('cv', 'skill'),)", 'object_name': 'CVSkill'},
            'cv': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'skills'", 'null': 'True', 'to': u"orm['cv.CV']"}),
            'desc': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'skill': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'cvs'", 'null': 'True', 'to': u"orm['cv.Skill']"})
        },
        u'cv.fl': {
            'Meta': {'unique_together': "(('cv', 'language'),)", 'object_name': 'FL'},
            'cv': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fl'", 'to': u"orm['cv.CV']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'spoken': ('django.db.models.fields.SmallIntegerField', [], {}),
            'written': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        u'cv.position': {
            'Meta': {'unique_together': "(('name',),)", 'object_name': 'Position'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_projects': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'permissions': ('django.db.models.fields.CharField', [], {'default': "'0000000000000000000000000000000000000000000000000000000'", 'max_length': '55'})
        },
        u'cv.prevproject': {
            'Meta': {'unique_together': "(('cv', 'title'),)", 'object_name': 'PrevProject'},
            'challenge': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'cv': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'prev_projects'", 'to': u"orm['cv.CV']"}),
            'date_finish': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_start': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'cv.prevscreenshot': {
            'Meta': {'object_name': 'PrevScreenshot'},
            'desc': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'screenshots'", 'to': u"orm['cv.PrevProject']"})
        },
        u'cv.skill': {
            'Meta': {'unique_together': "(('name',),)", 'object_name': 'Skill'},
            'desc': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'on_main': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
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

    complete_apps = ['cv']