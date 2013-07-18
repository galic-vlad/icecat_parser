#-*- coding: UTF-8 -*-
# import urllib2
# import base64
from lxml import etree
from django.db import models
from iceparser.models.utils import make_model_dict
from django.forms.models import model_to_dict


class Language(models.Model):
    code = models.CharField(max_length=20)
    short_code = models.CharField(max_length=5)
    published = models.CharField(max_length=1)

    def __unicode__(self):
        return self.code

    @classmethod
    def import_from_icecat(cls):
        from iceparser.models import Vocabulary

        # request = urllib2.Request(
        #     'http://data.icecat.biz/export/freexml/refs/LanguageList.xml.gz')
        # base64string = base64.encodestring(
        # '%s:%s' % ('username', 'password')).replace('\n', '')
        # request.add_header('Authorization', "Basic %s" % base64string)
        # result = urllib2.urlopen(request)
        #
        # local_file = open('languages.gz', "wb")
        # local_file.write(result.read())
        # local_file.close()

        tree = etree.parse('LanguageList.xml')

        current_languages = make_model_dict(Language)
        current_vocabularies = make_model_dict(Vocabulary)
        languages = {}

        # Save languages
        language_tags = tree.findall('.//Language')
        language_count = len(language_tags)
        for idx, language_tag in enumerate(language_tags):
            print '{0} de {1}'.format(idx+1, language_count)

            d = language_tag.attrib

            language = Language(
                id=int(d['ID']),
                code=d['Code'],
                short_code=d['ShortCode'],
                published='Y'
            )

            current_language = current_languages[language.id]

            if model_to_dict(language) != model_to_dict(current_language):
                language.save()

            languages[language.id] = language

        # Save translations
        Vocabulary.batch_import(
            tree.findall('.//Name'),
            current_vocabularies,
            current_languages
        )

    class Meta:
        app_label = 'iceparser'