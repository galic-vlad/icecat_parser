from django.contrib.auth.admin import admin
from iceparser.models import Language, Vocabulary, Measure, \
    MeasureSign, Tex, Feature

admin.site.register(Feature)
admin.site.register(Language)
admin.site.register(Measure)
admin.site.register(MeasureSign)
admin.site.register(Tex)
admin.site.register(Vocabulary)