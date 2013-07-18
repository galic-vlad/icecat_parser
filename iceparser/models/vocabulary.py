#-*- coding: UTF-8 -*-
from django.db import models
from django.forms import model_to_dict


class Vocabulary(models.Model):
    language = models.ForeignKey('Language')
    value = models.CharField(max_length=255)

    def __unicode__(self):
        return u'{0}: {1}'.format(self.language, self.value)

    @classmethod
    def batch_import(cls, tags, current_vocabularies, current_languages):
        result = []

        for vocabulary_tag in tags:
            voc_dict = vocabulary_tag.attrib

            if voc_dict['ID'] == '0':
                continue

            value = vocabulary_tag.text
            if not value:
                value = ''

            vocabulary = Vocabulary(
                id=int(voc_dict['ID']),
                language=current_languages[int(voc_dict['langid'])],
                value=value
            )

            try:
                if model_to_dict(vocabulary) != model_to_dict(current_vocabularies[vocabulary.id]):
                    vocabulary.save()
            except KeyError:
                vocabulary.save()

            result.append(vocabulary)

        return result

    class Meta:
        app_label = 'iceparser'