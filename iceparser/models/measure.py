#-*- coding: UTF-8 -*-
# import base64
# import urllib2
from lxml import etree
from django.db import models
from django.forms.models import model_to_dict
from iceparser.models.utils import make_model_dict


class Measure(models.Model):
    descriptions = models.ManyToManyField('Tex')
    names = models.ManyToManyField('Vocabulary')
    sign = models.CharField(max_length=255, default='')

    @classmethod
    def import_from_icecat(cls):
        from iceparser.models import Language, MeasureSign, Vocabulary, Tex

        # request = urllib2.Request(
        #     'http://data.icecat.biz/export/freexml/refs/MeasuresList.xml.gz')
        # base64string = base64.encodestring(
        # '%s:%s' % ('username', 'password')).replace('\n', '')
        # request.add_header('Authorization', "Basic %s" % base64string)
        # result = urllib2.urlopen(request)
        #
        # local_file = open('measures.gz', "wb")
        # local_file.write(result.read())
        # local_file.close()

        tree = etree.parse('MeasuresList.xml')

        languages = make_model_dict(Language)
        texes = make_model_dict(Tex)
        vocabularies = make_model_dict(Vocabulary)
        measure_signs = make_model_dict(MeasureSign)

        measures = tree.findall('.//Measure')
        measure_count = len(measures)

        # Save measures
        for idx, measure_tag in enumerate(measures):
            print '{0} de {1}'.format(idx + 1, measure_count)

            if measure_tag.find('Sign') is not None:
                sign_value = measure_tag.find('Sign').text
            else:
                sign_value = ''

            measure = Measure(
                id=measure_tag.attrib['ID'],
                sign=sign_value
            )

            measure.save()

            descs = Tex.batch_import(
                measure_tag.iterfind('.//Description'),
                texes,
                languages
            )

            current_descriptions = set([d.id for d in measure.descriptions.all()])
            new_descriptions = set([d.id for d in descs])
            if current_descriptions != new_descriptions:
                measure.descriptions = descs

            names = Vocabulary.batch_import(
                measure_tag.findall('.//Name'),
                vocabularies,
                languages
            )

            current_names = set([d.id for d in measure.names.all()])
            new_names = set([d.id for d in names])
            if current_names != new_names:
                measure.names = names

            # Save measure signs
            for measure_sign_tag in measure_tag.iterfind('Signs//Sign'):
                ms_dict = measure_sign_tag.attrib

                if ms_dict['ID'] == '0':
                    continue

                value = measure_sign_tag.text
                if not value:
                    value = ''

                measure_sign = MeasureSign(
                    id=int(ms_dict['ID']),
                    measure=measure,
                    language=languages[int(ms_dict['langid'])],
                    value=value
                )

                d1 = model_to_dict(measure_sign)

                try:
                    d2 = model_to_dict(measure_signs[measure_sign.id])

                    if d1 != d2 and int(d1['measure']) != d2['measure']:
                        measure_sign.save()
                except KeyError:
                    measure_sign.save()

    def __unicode__(self):
        return u'{0} - {1}'.format(self.id, self.sign)

    class Meta:
        app_label = 'iceparser'