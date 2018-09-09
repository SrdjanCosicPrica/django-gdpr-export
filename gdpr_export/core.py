# coding=utf-8
from django.db import models
from django.template.loader import render_to_string

from gdpr_export.models import GDPRExportField


def export_data(_object):
    assert isinstance(_object, models.Model)

    gdpr_export_fields = []
    for field in _object._meta.get_fields():
        if isinstance(field, GDPRExportField):
            gdpr_export_fields.append(field)

    if len(gdpr_export_fields) == 0:
        raise Exception('Did not find a field of type "GDPRExportField". The export method'
                        'will not know where to save files without it.')
    if len(gdpr_export_fields) > 1:
        raise Exception(
            'Found more than one field of type "GDPRExportField". Only one is permitted')

    objects = {}
    _perform_export(_object, objects)
    rendered = render_to_string(
        'gdpr_export.html',
        {'objects': objects, 'names': list(objects.keys()), 'download': True}
    )
    with open('abc.html', 'w') as f:
        f.write(rendered)


def _perform_export(_object, traversed_objects):
    # For testing purposes
    assert isinstance(_object, models.Model)
    _type = type(_object).__name__
    traversed = traversed_objects.get(_type, {})
    traversed_id_arr = traversed.get('ids', [])
    objects = traversed.get('objects', [])
    if _object.id in traversed_id_arr:
        return None
    traversed_id_arr.append(_object.id)
    objects.append(_object)
    traversed_objects.update({_type: {'ids': traversed_id_arr, 'objects': objects}})

    for field in _object._meta.get_fields():
        if field.is_relation:
            related_data, is_queryset = _get_related_data(_object, field)

            if is_queryset:
                for _obj in related_data:
                    _perform_export(_obj, traversed_objects)
            else:
                _perform_export(related_data, traversed_objects)
        else:
            # TODO: Check for File fields, save other field values
            pass


def _get_related_data(_object, field):
    """
    :param field: A related field (ForeignKey, OneToOne, M2M)
    :return: {QuerySet} or Model Instance, boolean indicating if it is a queryset
    """
    name = field.name
    has_related_name = getattr(field, 'related_name', None) is not None
    if has_related_name:
        name = field.related_name

    if field.one_to_one or field.many_to_one:
        return getattr(_object, name), False

    if not field.concrete and not has_related_name:
        name = '{}_set'.format(name)
    return getattr(_object, name).all(), True

