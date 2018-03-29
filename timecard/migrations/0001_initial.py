# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'User'
        db.create_table(u'timecard_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('surname', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('login', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('accessLevel', self.gf('django.db.models.fields.CharField')(default=0, max_length=1)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('office', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('dep', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('avator', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('email', self.gf('django.db.models.fields.EmailField')(default='@minsk.ximxim.com', max_length=150)),
            ('fb', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('twitter', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('skype', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('hb', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('gender', self.gf('django.db.models.fields.CharField')(default=1, max_length=2)),
            ('ua', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('profession', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('counter01', self.gf('django.db.models.fields.IntegerField')()),
            ('group', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('voted', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'timecard', ['User'])

        # Adding model 'UserTime'
        db.create_table(u'timecard_usertime', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_id', self.gf('django.db.models.fields.IntegerField')()),
            ('time', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'timecard', ['UserTime'])

        # Adding model 'UserDepartament'
        db.create_table(u'timecard_userdepartament', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'timecard', ['UserDepartament'])

        # Adding model 'UserProfession'
        db.create_table(u'timecard_userprofession', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'timecard', ['UserProfession'])

        # Adding model 'UserRoles'
        db.create_table(u'timecard_userroles', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'timecard', ['UserRoles'])

        # Adding model 'UserModule'
        db.create_table(u'timecard_usermodule', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_id', self.gf('django.db.models.fields.IntegerField')()),
            ('mod', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('position', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('show', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'timecard', ['UserModule'])

        # Adding model 'UserPost'
        db.create_table(u'timecard_userpost', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.TextField')()),
            ('body', self.gf('django.db.models.fields.CharField')(max_length=20000)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'timecard', ['UserPost'])

        # Adding model 'UserPostComment'
        db.create_table(u'timecard_userpostcomment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('post_id', self.gf('django.db.models.fields.IntegerField')()),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('author', self.gf('django.db.models.fields.TextField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'timecard', ['UserPostComment'])

        # Adding model 'CalendarDaysOff'
        db.create_table(u'timecard_calendardaysoff', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.IntegerField')()),
            ('office', self.gf('django.db.models.fields.CharField')(max_length=2)),
        ))
        db.send_create_signal(u'timecard', ['CalendarDaysOff'])

        # Adding model 'UserMissedHours'
        db.create_table(u'timecard_usermissedhours', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('umess', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('date', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('status', self.gf('django.db.models.fields.IntegerField')()),
            ('lock_person', self.gf('django.db.models.fields.CharField')(max_length=70)),
        ))
        db.send_create_signal(u'timecard', ['UserMissedHours'])

        # Adding model 'Boss_notice'
        db.create_table(u'timecard_boss_notice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.IntegerField')()),
            ('date', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('notice', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal(u'timecard', ['Boss_notice'])

        # Adding model 'User_duty'
        db.create_table(u'timecard_user_duty', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.IntegerField')()),
            ('date', self.gf('django.db.models.fields.CharField')(max_length=25)),
        ))
        db.send_create_signal(u'timecard', ['User_duty'])

        # Adding model 'Projects'
        db.create_table(u'timecard_projects', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project_name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('project_desc', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('project_opened', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'timecard', ['Projects'])

        # Adding model 'UserProjectAssignments'
        db.create_table(u'timecard_userprojectassignments', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.IntegerField')()),
            ('date', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('project', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'timecard', ['UserProjectAssignments'])

        # Adding model 'Reports'
        db.create_table(u'timecard_reports', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('week', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('year', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('reporting_date', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('user_id', self.gf('django.db.models.fields.IntegerField')()),
            ('user_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('user_surname', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('office', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('dep', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('project_name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('report', self.gf('django.db.models.fields.CharField')(max_length=10000)),
            ('employee_feedback', self.gf('django.db.models.fields.CharField')(max_length=5000)),
            ('lead_feedback', self.gf('django.db.models.fields.CharField')(max_length=5000)),
            ('hours', self.gf('django.db.models.fields.IntegerField')()),
            ('overtimed', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'timecard', ['Reports'])

        # Adding model 'Votes'
        db.create_table(u'timecard_votes', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('votes_yes', self.gf('django.db.models.fields.IntegerField')()),
            ('votes_no', self.gf('django.db.models.fields.IntegerField')()),
            ('votes_dontcare', self.gf('django.db.models.fields.IntegerField')()),
            ('votes_yes_desc', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('votes_no_desc', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('votes_dontcare_desc', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('office', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('archived', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('votes_yes_who', self.gf('django.db.models.fields.CharField')(max_length=5000)),
            ('votes_no_who', self.gf('django.db.models.fields.CharField')(max_length=5000)),
            ('votes_dontcare_who', self.gf('django.db.models.fields.CharField')(max_length=5000)),
        ))
        db.send_create_signal(u'timecard', ['Votes'])

        # Adding model 'ProjectThread'
        db.create_table(u'timecard_projectthread', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_id', self.gf('django.db.models.fields.IntegerField')()),
            ('user_name_surname', self.gf('django.db.models.fields.CharField')(max_length=71)),
            ('user_role', self.gf('django.db.models.fields.IntegerField')()),
            ('project_id', self.gf('django.db.models.fields.IntegerField')()),
            ('who_assigned', self.gf('django.db.models.fields.CharField')(max_length=71)),
            ('who_unassigned', self.gf('django.db.models.fields.CharField')(max_length=71)),
        ))
        db.send_create_signal(u'timecard', ['ProjectThread'])

        # Adding model 'Offices'
        db.create_table(u'timecard_offices', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('full_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('boss_email', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('mass_email', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('time_shift', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('weather_script', self.gf('django.db.models.fields.CharField')(max_length=1000)),
        ))
        db.send_create_signal(u'timecard', ['Offices'])

        # Adding model 'Reservation_Categories'
        db.create_table(u'timecard_reservation_categories', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('office', self.gf('django.db.models.fields.CharField')(max_length=2)),
        ))
        db.send_create_signal(u'timecard', ['Reservation_Categories'])

        # Adding model 'Reservation_Objects'
        db.create_table(u'timecard_reservation_objects', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['timecard.Reservation_Categories'], db_index=False)),
            ('is_avaliable', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['timecard.User'], db_index=False)),
        ))
        db.send_create_signal(u'timecard', ['Reservation_Objects'])

        # Adding model 'Reservation_History'
        db.create_table(u'timecard_reservation_history', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('obj', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['timecard.Reservation_Objects'], db_index=False)),
            ('event', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('user', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('status', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'timecard', ['Reservation_History'])


    def backwards(self, orm):
        # Deleting model 'User'
        db.delete_table(u'timecard_user')

        # Deleting model 'UserTime'
        db.delete_table(u'timecard_usertime')

        # Deleting model 'UserDepartament'
        db.delete_table(u'timecard_userdepartament')

        # Deleting model 'UserProfession'
        db.delete_table(u'timecard_userprofession')

        # Deleting model 'UserRoles'
        db.delete_table(u'timecard_userroles')

        # Deleting model 'UserModule'
        db.delete_table(u'timecard_usermodule')

        # Deleting model 'UserPost'
        db.delete_table(u'timecard_userpost')

        # Deleting model 'UserPostComment'
        db.delete_table(u'timecard_userpostcomment')

        # Deleting model 'CalendarDaysOff'
        db.delete_table(u'timecard_calendardaysoff')

        # Deleting model 'UserMissedHours'
        db.delete_table(u'timecard_usermissedhours')

        # Deleting model 'Boss_notice'
        db.delete_table(u'timecard_boss_notice')

        # Deleting model 'User_duty'
        db.delete_table(u'timecard_user_duty')

        # Deleting model 'Projects'
        db.delete_table(u'timecard_projects')

        # Deleting model 'UserProjectAssignments'
        db.delete_table(u'timecard_userprojectassignments')

        # Deleting model 'Reports'
        db.delete_table(u'timecard_reports')

        # Deleting model 'Votes'
        db.delete_table(u'timecard_votes')

        # Deleting model 'ProjectThread'
        db.delete_table(u'timecard_projectthread')

        # Deleting model 'Offices'
        db.delete_table(u'timecard_offices')

        # Deleting model 'Reservation_Categories'
        db.delete_table(u'timecard_reservation_categories')

        # Deleting model 'Reservation_Objects'
        db.delete_table(u'timecard_reservation_objects')

        # Deleting model 'Reservation_History'
        db.delete_table(u'timecard_reservation_history')


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
            'project_opened': ('django.db.models.fields.IntegerField', [], {})
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