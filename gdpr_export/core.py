# coding=utf-8
from django.db import models

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

    objects = _perform_export(_object, {})
    print('objects', objects)


def _perform_export(_object, traversed_objects):
    # For testing purposes
    assert isinstance(_object, models.Model)
    _type = type(_object).__name__
    traversed_id_arr = traversed_objects.get(_type, [])
    if _object.id in traversed_id_arr:
        return None
    traversed_id_arr.append(_object.id)
    traversed_objects.update({_type: traversed_id_arr})

    data = [_object]
    for field in _object._meta.get_fields():
        if field.is_relation:
            related_data, is_queryset = _get_related_data(_object, field)

            if is_queryset:
                for _obj in related_data:
                    tmp = _perform_export(_obj, traversed_objects)
                    if tmp is not None:
                        data.extend(tmp)
            else:
                tmp = _perform_export(related_data, traversed_objects)
                if tmp is not None:
                    data.extend(tmp)
        else:
            # TODO: Check for File fields, save other field values
            pass
    return data


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

