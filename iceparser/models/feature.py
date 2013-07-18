#-*- coding: UTF-8 -*-
from django.forms import model_to_dict
from lxml import etree
from django.db import models
from iceparser.models.utils import make_model_dict


class Feature(models.Model):
    klass = models.IntegerField()
    type = models.CharField(max_length=60)
    measure = models.ForeignKey('Measure')
    descriptions = models.ManyToManyField('Tex')
    names = models.ManyToManyField('Vocabulary')

    def __unicode__(self):
        return u'{0} - {1}'.format(self.type, self.measure)

    @classmethod
    def import_from_icecat(cls):
        from iceparser.models import Language, Measure, Tex, Vocabulary

        tree = etree.parse('FeaturesList.xml')

        current_measures = make_model_dict(Measure)
        current_features = make_model_dict(Feature)
        current_languages = make_model_dict(Language)
        current_texes = make_model_dict(Tex)
        current_vocabularies = make_model_dict(Vocabulary)

        # Save features
        feature_tags = tree.findall('.//Feature')
        features_count = len(feature_tags)
        for idx, feature_tag in enumerate(feature_tags):
            print '{0} de {1}'.format(idx+1, features_count)

            d = feature_tag.attrib

            measure_tag = feature_tag.find('Measure')
            if not measure_tag:
                continue

            measure_id = int(measure_tag.attrib['ID'])
            measure = current_measures[measure_id]

            feature = Feature(
                id=int(d['ID']),
                klass=int(d['Class']),
                type=d['Type'],
                measure=measure
            )

            try:
                if model_to_dict(feature) != model_to_dict(current_features[feature.id]):
                    feature.save()
            except KeyError:
                feature.save()

            descs = Tex.batch_import(
                feature_tag.iterfind('.//Description'),
                current_texes,
                current_languages
            )

            current_descriptions = set(
                [d.id for d in measure.descriptions.all()])
            new_descriptions = set([d.id for d in descs])
            if current_descriptions != new_descriptions:
                measure.descriptions = descs

            names = Vocabulary.batch_import(
                feature_tag.findall('.//Name'),
                current_vocabularies,
                current_languages
            )

            current_names = set([d.id for d in measure.names.all()])
            new_names = set([d.id for d in names])
            if current_names != new_names:
                measure.names = names

    class Meta:
        app_label = 'iceparser'
