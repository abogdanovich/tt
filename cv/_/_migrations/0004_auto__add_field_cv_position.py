# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'CV.position'
        db.add_column('cv_cv', 'position',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cv.Position'], null=True, blank=True),
                      keep_default=False)

        # Removing M2M table for field position on 'CV'
        db.delete_table('cv_cv_position')


    def backwards(self, orm):
        # Deleting field 'CV.position'
        db.delete_column('cv_cv', 'position_id')

        # Adding M2M table for field position on 'CV'
        db.create_table('cv_cv_position', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('cv', models.ForeignKey(orm['cv.cv'], null=False)),
            ('position', models.ForeignKey(orm['cv.position'], null=False))
        ))
        db.create_unique('cv_cv_position', ['cv_id', 'position_id'])


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
        'cv.cvskill': {
            'Meta': {'unique_together': "(('cv', 'skill'),)", 'object_name': 'CVSkill'},
            'cv': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'skills'", 'to': "orm['cv.CV']"}),
            'desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'skill': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'cv_skills'", 'null': 'True', 'blank': 'True', 'to': "orm['cv.Skill']"})
        },
        'cv.fl': {
            'Meta': {'unique_together': "(('cv', 'language'),)", 'object_name': 'FL'},
            'cv': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fl'", 'to': "orm['cv.CV']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'spoken': ('django.db.models.fields.SmallIntegerField', [], {}),
            'written': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        'cv.position': {
            'Meta': {'unique_together': "(('name',),)", 'object_name': 'Position'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'skills': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'positions'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['cv.Skill']"})
        },
        'cv.skill': {
            'Meta': {'unique_together': "(('name',),)", 'object_name': 'Skill'},
            'desc': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
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
