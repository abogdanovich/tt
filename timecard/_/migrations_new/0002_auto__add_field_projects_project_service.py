# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Projects.project_service'
        db.add_column(u'timecard_projects', 'project_service',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Projects.project_service'
        db.delete_column(u'timecard_projects', 'project_service')


    models = {
        u'timecard.boss_notice': {
            'Meta': {'object_name': 'Boss_notice'},
            'date': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notice': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'user': ('django.db.models.fields.IntegerField', [], {})
        },
        u'timecard.calendardaysoff': {
            'Meta': {'object_name': 'CalendarDaysOff'},
            'date': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'office': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        u'timecard.offices': {
            'Meta': {'object_name': 'Offices'},
            'boss_email': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mass_email': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'time_shift': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'weather_script': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        },
        u'timecard.projects': {
            'Meta': {'object_name': 'Projects'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project_desc': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'project_name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'project_opened': ('django.db.models.fields.IntegerField', [], {}),
            'project_service': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'timecard.projectthread': {
            'Meta': {'object_name': 'ProjectThread'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project_id': ('django.db.models.fields.IntegerField', [], {}),
            'user_id': ('django.db.models.fields.IntegerField', [], {}),
            'user_name_surname': ('django.db.models.fields.CharField', [], {'max_length': '71'}),
            'user_role': ('django.db.models.fields.IntegerField', [], {}),
            'who_assigned': ('django.db.models.fields.CharField', [], {'max_length': '71'}),
            'who_unassigned': ('django.db.models.fields.CharField', [], {'max_length': '71'})
        },
        u'timecard.reports': {
            'Meta': {'object_name': 'Reports'},
            'dep': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'employee_feedback': ('django.db.models.fields.CharField', [], {'max_length': '5000'}),
            'hours': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lead_feedback': ('django.db.models.fields.CharField', [], {'max_length': '5000'}),
            'office': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'overtimed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'project_name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'report': ('django.db.models.fields.CharField', [], {'max_length': '10000'}),
            'reporting_date': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'user_id': ('django.db.models.fields.IntegerField', [], {}),
            'user_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'user_surname': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'week': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'year': ('django.db.models.fields.CharField', [], {'max_length': '4'})
        },
        u'timecard.reservation_categories': {
            'Meta': {'object_name': 'Reservation_Categories'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'office': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        u'timecard.reservation_history': {
            'Meta': {'object_name': 'Reservation_History'},
            'event': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'obj': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['timecard.Reservation_Objects']", 'db_index': 'False'}),
            'status': ('django.db.models.fields.BooleanField', [], {}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'timecard.reservation_objects': {
            'Meta': {'object_name': 'Reservation_Objects'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['timecard.Reservation_Categories']", 'db_index': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_avaliable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['timecard.User']", 'db_index': 'False'})
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
        },
        u'timecard.user_duty': {
            'Meta': {'object_name': 'User_duty'},
            'date': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.IntegerField', [], {})
        },
        u'timecard.userdepartament': {
            'Meta': {'object_name': 'UserDepartament'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'timecard.usermissedhours': {
            'Meta': {'object_name': 'UserMissedHours'},
            'date': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lock_person': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'umess': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'timecard.usermodule': {
            'Meta': {'object_name': 'UserModule'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mod': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'show': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user_id': ('django.db.models.fields.IntegerField', [], {})
        },
        u'timecard.userpost': {
            'Meta': {'object_name': 'UserPost'},
            'author': ('django.db.models.fields.TextField', [], {}),
            'body': ('django.db.models.fields.CharField', [], {'max_length': '20000'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'timecard.userpostcomment': {
            'Meta': {'object_name': 'UserPostComment'},
            'author': ('django.db.models.fields.TextField', [], {}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post_id': ('django.db.models.fields.IntegerField', [], {})
        },
        u'timecard.userprofession': {
            'Meta': {'object_name': 'UserProfession'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'timecard.userprojectassignments': {
            'Meta': {'object_name': 'UserProjectAssignments'},
            'date': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.IntegerField', [], {})
        },
        u'timecard.userroles': {
            'Meta': {'object_name': 'UserRoles'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'timecard.usertime': {
            'Meta': {'object_name': 'UserTime'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time': ('django.db.models.fields.IntegerField', [], {}),
            'user_id': ('django.db.models.fields.IntegerField', [], {})
        },
        u'timecard.votes': {
            'Meta': {'object_name': 'Votes'},
            'archived': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'office': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'votes_dontcare': ('django.db.models.fields.IntegerField', [], {}),
            'votes_dontcare_desc': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'votes_dontcare_who': ('django.db.models.fields.CharField', [], {'max_length': '5000'}),
            'votes_no': ('django.db.models.fields.IntegerField', [], {}),
            'votes_no_desc': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'votes_no_who': ('django.db.models.fields.CharField', [], {'max_length': '5000'}),
            'votes_yes': ('django.db.models.fields.IntegerField', [], {}),
            'votes_yes_desc': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'votes_yes_who': ('django.db.models.fields.CharField', [], {'max_length': '5000'})
        }
    }

    complete_apps = ['timecard']