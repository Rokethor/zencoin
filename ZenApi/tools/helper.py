from db import Document
from db import ListField
from db import EmbeddedDocumentField
from db import DictField
from db import DateTimeField
from db import ComplexDateTimeField
from db import StringField
from db import FloatField
from db import IntField
from db import BooleanField
from db import ObjectIdField
from db import DecimalField
from db import ReferenceField

def mongo_to_dict(obj, exclude_fields=[]):
    return_data = []
    if obj is None:
        return None
    if isinstance(obj, Document):
        return_data.append(("id",str(obj.id)))
    for field_name in obj._fields:
        if field_name in exclude_fields:
            continue
        if field_name in ("id",):
            continue
        data = obj._data[field_name]
        if isinstance(obj._fields[field_name], ListField):
            return_data.append((field_name, list_field_to_dict(data, exclude_fields)))
        elif isinstance(obj._fields[field_name], EmbeddedDocumentField):
            return_data.append((field_name, mongo_to_dict(data, exclude_fields)))
        elif isinstance(obj._fields[field_name], ReferenceField):
            return_data.append((field_name.replace('_id', ''), mongo_to_dict(data, exclude_fields)))
        elif isinstance(obj._fields[field_name], DictField):
            return_data.append((field_name, data))
        else:
            return_data.append((field_name, mongo_to_python_type(obj._fields[field_name],data)))
    return dict(return_data)

def list_field_to_dict(list_field, exclude_fields=[]):
    return_data = []
    for item in list_field:
        if isinstance(item, EmbeddedDocument):
            return_data.append(mongo_to_dict(item, exclude_fields))
        else:
            return_data.append(mongo_to_python_type(item, item))
    return return_data

def mongo_to_python_type(field, data):
    if isinstance(field, DateTimeField):
        return str(data.strftime("%d/%m/%Y %H:%M"))
    elif isinstance(field, ComplexDateTimeField):
        return field.to_python(data).isoformat()
    elif isinstance(field, StringField):
        return str(data)
    elif isinstance(field, FloatField):
        return float(data)
    elif isinstance(field, IntField):
        return int(data)
    elif isinstance(field, BooleanField):
        return bool(data)
    elif isinstance(field, ObjectIdField):
        return str(data)
    elif isinstance(field, DecimalField):
        return data
    return str(data)
