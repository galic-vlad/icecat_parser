#-*- coding: UTF-8 -*-
from django.db import models
from django.forms import model_to_dict


class Tex(models.Model):
    language = models.ForeignKey('Language')
    value = models.TextField(default='')

    def __unicode__(self):
        return u'{0}: {1}'.format(self.language, self.value)

    @classmethod
    def batch_import(cls, tags, current_texs, current_languages):
        result = []
        for tex_tag in tags:
            tex_dict = tex_tag.attrib

            if tex_dict['ID'] == '0':
                continue

            value = tex_tag.text
            if not value:
                value = ''

            tex = Tex(
                id=int(tex_dict['ID']),
                language=current_languages[int(tex_dict['langid'])],
                value=value
            )

            try:
                if model_to_dict(tex) != model_to_dict(current_texs[tex.id]):
                    tex.save()
            except KeyError:
                tex.save()

            result.append(tex)

        return result

    class Meta:
        app_label = 'iceparser'