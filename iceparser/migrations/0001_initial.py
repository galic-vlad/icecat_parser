# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Language'
        db.create_table(u'iceparser_language', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('short_code', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('published', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('iceparser', ['Language'])

        # Adding model 'Tex'
        db.create_table(u'iceparser_tex', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['iceparser.Language'])),
            ('value', self.gf('django.db.models.fields.TextField')(default='')),
        ))
        db.send_create_signal('iceparser', ['Tex'])

        # Adding model 'Measure'
        db.create_table(u'iceparser_measure', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sign', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
        ))
        db.send_create_signal('iceparser', ['Measure'])

        # Adding M2M table for field descriptions on 'Measure'
        m2m_table_name = db.shorten_name(u'iceparser_measure_descriptions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('measure', models.ForeignKey(orm['iceparser.measure'], null=False)),
            ('tex', models.ForeignKey(orm['iceparser.tex'], null=False))
        ))
        db.create_unique(m2m_table_name, ['measure_id', 'tex_id'])

        # Adding M2M table for field names on 'Measure'
        m2m_table_name = db.shorten_name(u'iceparser_measure_names')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('measure', models.ForeignKey(orm['iceparser.measure'], null=False)),
            ('vocabulary', models.ForeignKey(orm['iceparser.vocabulary'], null=False))
        ))
        db.create_unique(m2m_table_name, ['measure_id', 'vocabulary_id'])

        # Adding model 'MeasureSign'
        db.create_table(u'iceparser_measuresign', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('measure', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['iceparser.Measure'])),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['iceparser.Language'])),
            ('value', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
        ))
        db.send_create_signal('iceparser', ['MeasureSign'])

        # Adding model 'Vocabulary'
        db.create_table(u'iceparser_vocabulary', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['iceparser.Language'])),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('iceparser', ['Vocabulary'])


    def backwards(self, orm):
        # Deleting model 'Language'
        db.delete_table(u'iceparser_language')

        # Deleting model 'Tex'
        db.delete_table(u'iceparser_tex')

        # Deleting model 'Measure'
        db.delete_table(u'iceparser_measure')

        # Removing M2M table for field descriptions on 'Measure'
        db.delete_table(db.shorten_name(u'iceparser_measure_descriptions'))

        # Removing M2M table for field names on 'Measure'
        db.delete_table(db.shorten_name(u'iceparser_measure_names'))

        # Deleting model 'MeasureSign'
        db.delete_table(u'iceparser_measuresign')

        # Deleting model 'Vocabulary'
        db.delete_table(u'iceparser_vocabulary')


    models = {
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