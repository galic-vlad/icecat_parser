# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Feature'
        db.create_table(u'iceparser_feature', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('klass', self.gf('django.db.models.fields.IntegerField')()),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('measure', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['iceparser.Measure'])),
        ))
        db.send_create_signal('iceparser', ['Feature'])

        # Adding M2M table for field descriptions on 'Feature'
        m2m_table_name = db.shorten_name(u'iceparser_feature_descriptions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('feature', models.ForeignKey(orm['iceparser.feature'], null=False)),
            ('tex', models.ForeignKey(orm['iceparser.tex'], null=False))
        ))
        db.create_unique(m2m_table_name, ['feature_id', 'tex_id'])

        # Adding M2M table for field names on 'Feature'
        m2m_table_name = db.shorten_name(u'iceparser_feature_names')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('feature', models.ForeignKey(orm['iceparser.feature'], null=False)),
            ('vocabulary', models.ForeignKey(orm['iceparser.vocabulary'], null=False))
        ))
        db.create_unique(m2m_table_name, ['feature_id', 'vocabulary_id'])


    def backwards(self, orm):
        # Deleting model 'Feature'
        db.delete_table(u'iceparser_feature')

        # Removing M2M table for field descriptions on 'Feature'
        db.delete_table(db.shorten_name(u'iceparser_feature_descriptions'))

        # Removing M2M table for field names on 'Feature'
        db.delete_table(db.shorten_name(u'iceparser_feature_names'))


    models = {
        'iceparser.feature': {
            'Meta': {'object_name': 'Feature'},
            'descriptions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['iceparser.Tex']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'klass': ('django.db.models.fields.IntegerField', [], {}),
            'measure': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['iceparser.Measure']"}),
            'names': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['iceparser.Vocabulary']", 'symmetrical': 'False'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'iceparser.language': {
            'Meta': {'object_name': 'Language'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'published': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'short_code': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        'iceparser.measure': {
            'Meta': {'object_name': 'Measure'},
            'descriptions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['iceparser.Tex']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'names': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['iceparser.Vocabulary']", 'symmetrical': 'False'}),
            'sign': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        },
        'iceparser.measuresign': {
            'Meta': {'object_name': 'MeasureSign'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['iceparser.Language']"}),
            'measure': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['iceparser.Measure']"}),
            'value': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        },
        'iceparser.tex': {
            'Meta': {'object_name': 'Tex'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['iceparser.Language']"}),
            'value': ('django.db.models.fields.TextField', [], {'default': "''"})
        },
        'iceparser.vocabulary': {
            'Meta': {'object_name': 'Vocabulary'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['iceparser.Language']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['iceparser']