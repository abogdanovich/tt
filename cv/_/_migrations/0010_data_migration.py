# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Remember to use orm['appname.ModelName'] rather than "from appname.models..."
        for cv in orm.CV.objects.all():
            if cv.user:
                cv.login = cv.user.login
                if cv.user.accessLevel == 4:
                    cv.accessLevel = 4
                else:
                    cv.accessLevel = 0
            else:
                cv.fired = True
            cv.save()


    def backwards(self, orm):
        "Write your backwards methods here."
        pass

    models = {
        'cv.cv': {
            'Meta': {'object_name': 'CV'},
            'accessLevel': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'edit_fl': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'edit_skills': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'fired': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'login': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'position': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'cvs'", 'null': 'True', 'to': "orm['cv.Position']"}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['timecard.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        'cv.cvskill': {
            'Meta': {'unique_together': "(('cv', 'skill'),)", 'object_name': 'CVSkill'},
            'cv': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'skills'", 'null': 'True', 'to': "orm['cv.CV']"}),
            'desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'skill': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'cvs'", 'null': 'True', 'to': "orm['cv.Skill']"})
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
            'in_projects': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'cv.skill': {
            'Meta': {'unique_together': "(('name',),)", 'object_name': 'Skill'},
            'desc': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'on_main': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
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
    symmetrical = True
