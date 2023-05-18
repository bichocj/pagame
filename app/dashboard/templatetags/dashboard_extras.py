from datetime import datetime, timedelta
from django.utils.safestring import mark_safe
from django import template

register = template.Library()


@register.filter
def get_columns_labels(view_model, colums):
    columns = []
    for column in colums:
        columns.append(view_model.get_serializer().fields[column].label)
    return columns


@register.filter
def get_column_label(view_model, column_name):
    if column_name in view_model.get_serializer().fields:
        return view_model.get_serializer().fields[column_name].label
    return column_name


@register.filter
def get_home_path(value):
    return value.get_serializer().get_home_path()


@register.filter
def get_model_name_plural(value):
    return value.get_serializer().Meta.model._meta.verbose_name_plural.title()


@register.filter
def get_model_name(value):
    return value.get_serializer().Meta.model._meta.verbose_name.title()


@register.filter
def active_if_path_match(keyword, request):
    if request.path.__contains__(keyword):
        return "active"
    return ""


@register.filter
def custom_class(column_label):
    vertical_columns_labels = (
        "Horas normales",
        "Importe horas normales",
        "Horas al 25%",
        "Importe horas al 25%",
        "Horas al 35%",
        "Importe horas al 35%",
    )
    if column_label in vertical_columns_labels:
        return "vertical-text"


@register.filter
def format_bool(value):
    if value is None or isinstance(value, bool):
        return "%s" % {True: "Si", False: "No", None: "ninguno"}[value]
    return value


#
# register.filter("get_columns_labels", get_columns_labels)
# register.filter("get_column_label", get_column_label)
# register.filter("get_model_name_plural", get_model_name_plural)
# register.filter("get_model_name", get_model_name)
# register.filter("get_home_path", get_home_path)
# register.filter("active_if_path_match", active_if_path_match)
# register.filter("custom_class", custom_class)
