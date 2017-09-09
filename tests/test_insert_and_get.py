from django.db import models

from .util import get_fake_model


def test_insert_and_get_m2m():
    """Ensures that creating objects with a m2m relationship
    works properly when using insert_and_get.

    This requires model_instance._state.db to be properly set,
    something that wasn't happening as reported in issue #25.
    """

    model1 = get_fake_model({
        'title': models.CharField(max_length=255)
    })

    model2 = get_fake_model({
        'name': models.CharField(max_length=255),
        'model1': models.ManyToManyField(model1)
    })

    obj1 = model1.objects.create(title='Henk')
    obj2 = model2.objects.upsert_and_get(
        conflict_target=['id'],
        fields={'name': 'Swen'}
    )

    obj2.model1.add(obj1)
    obj2.save()

    obj2.refresh_from_db()

    assert obj2.model1.count() == 1
    assert obj2.model1.first().title == 'Henk'
