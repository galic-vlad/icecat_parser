def make_model_dict(cls):
    return dict([(e.id, e) for e in cls.objects.all()])


def instance_equals(i1, i2):
    pass