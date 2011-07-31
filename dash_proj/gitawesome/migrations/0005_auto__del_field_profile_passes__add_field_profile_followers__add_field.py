# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Profile.passes'
        db.delete_column('gitawesome_profile', 'passes')

        # Adding field 'Profile.followers'
        db.add_column('gitawesome_profile', 'followers', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding field 'Profile.following'
        db.add_column('gitawesome_profile', 'following', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding field 'Profile.gists'
        db.add_column('gitawesome_profile', 'gists', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding field 'Profile.repos'
        db.add_column('gitawesome_profile', 'repos', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding field 'Profile.location'
        db.add_column('gitawesome_profile', 'location', self.gf('django.db.models.fields.CharField')(default='', max_length=128, blank=True), keep_default=False)

        # Adding field 'Profile.company'
        db.add_column('gitawesome_profile', 'company', self.gf('django.db.models.fields.CharField')(default='', max_length=128, blank=True), keep_default=False)

        # Adding field 'Profile.blog'
        db.add_column('gitawesome_profile', 'blog', self.gf('django.db.models.fields.CharField')(default='', max_length=128, blank=True), keep_default=False)

        # Adding field 'Profile.date_joined'
        db.add_column('gitawesome_profile', 'date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 7, 31, 1, 30, 37, 930360)), keep_default=False)


    def backwards(self, orm):
        
        # Adding field 'Profile.passes'
        db.add_column('gitawesome_profile', 'passes', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Deleting field 'Profile.followers'
        db.delete_column('gitawesome_profile', 'followers')

        # Deleting field 'Profile.following'
        db.delete_column('gitawesome_profile', 'following')

        # Deleting field 'Profile.gists'
        db.delete_column('gitawesome_profile', 'gists')

        # Deleting field 'Profile.repos'
        db.delete_column('gitawesome_profile', 'repos')

        # Deleting field 'Profile.location'
        db.delete_column('gitawesome_profile', 'location')

        # Deleting field 'Profile.company'
        db.delete_column('gitawesome_profile', 'company')

        # Deleting field 'Profile.blog'
        db.delete_column('gitawesome_profile', 'blog')

        # Deleting field 'Profile.date_joined'
        db.delete_column('gitawesome_profile', 'date_joined')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'gitawesome.commit': {
            'Meta': {'object_name': 'Commit'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'points': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gitawesome.Project']"}),
            'sha': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'gitawesome.profile': {
            'Meta': {'object_name': 'Profile'},
            'avatar_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'blog': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'}),
            'company': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {}),
            'followers': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'following': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'gists': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'}),
            'points': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'repos': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '256', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'gitawesome.project': {
            'Meta': {'object_name': 'Project'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '256', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['gitawesome']
