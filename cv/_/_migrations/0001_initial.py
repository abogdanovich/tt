# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CV'
        db.create_table('cv_cv', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='cv', null=True, default=None, to=orm['timecard.User'], blank=True, unique=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('surname', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('position', self.gf('django.db.models.fields.CharField')(default='no data...', max_length=100)),
            ('edit_fl', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('edit_skills', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('cv', ['CV'])

        # Adding model 'FL'
        db.create_table('cv_fl', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cv', self.gf('django.db.models.fields.related.ForeignKey')(related_name='fl', to=orm['cv.CV'])),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('spoken', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('written', self.gf('django.db.models.fields.SmallIntegerField')()),
        ))
        db.send_create_signal('cv', ['FL'])

        # Adding model 'Skill'
        db.create_table('cv_skill', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('cv', ['Skill'])

        # Adding model 'CVSkill'
        db.create_table('cv_cvskill', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cv', self.gf('django.db.models.fields.related.ForeignKey')(related_name='cv_skills', to=orm['cv.CV'])),
            ('skill', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='cv_skills', null=True, blank=True, to=orm['cv.Skill'])),
            ('desc', self.gf('django.db.models.fields.TextField')(default='no data...', blank=True)),
        ))
        db.send_create_signal('cv', ['CVSkill'])

        # Adding unique constraint on 'CVSkill', fields ['cv', 'skill']
        db.create_unique('cv_cvskill', ['cv_id', 'skill_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'CVSkill', fields ['cv', 'skill']
        db.delete_unique('cv_cvskill', ['cv_id', 'skill_id'])

        # Deleting model 'CV'
        db.delete_table('cv_cv')

        # Deleting model 'FL'
        db.delete_table('cv_fl')

        # Deleting model 'Skill'
        db.delete_table('cv_skill')

        # Deleting model 'CVSkill'
        db.delete_table('cv_cvskill')


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
        'cv.cvskill': {
            'Meta': {'unique_together': "(('cv', 'skill'),)", 'object_name': 'CVSkill'},
            'cv': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cv_skills'", 'to': "orm['cv.CV']"}),
            'desc': ('django.db.models.fields.TextField', [], {'default': "'no data...'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'skill': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'cv_skills'", 'null': 'True', 'blank': 'True', 'to': "orm['cv.Skill']"})
        },
        'cv.fl': {
            'Meta': {'object_name': 'FL'},
            'cv': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fl'", 'to': "orm['cv.CV']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'spoken': ('django.db.models.fields.SmallIntegerField', [], {}),
            'written': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        'cv.skill': {
            'Meta': {'object_name': 'Skill'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
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

    complete_apps = ['cv']
