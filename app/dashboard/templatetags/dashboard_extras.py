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
        "S/. horas normales",
        "Horas al 25%",
        "S/. horas al 25%",
        "Horas al 35%",
        "S/. horas al 35%",
    )
    if column_label in vertical_columns_labels:
        return "vertical-text"


@register.filter
def format_bool(value):
    if value is None or isinstance(value, bool):
        return "%s" % {True: "Si", False: "No", None: ""}[value]
    return value


@register.filter
def format_None(value):
    if value is None:
        return ""
    return value


@register.filter
def get_month_name_by_number(value):
    month_dict = {
        1: "Enenro",
        2: "Febrero",
        3: "Marzo",
        4: "Abril",
        5: "Mayo",
        6: "Junio",
        7: "Julio",
        8: "Agosto",
        9: "Septiembre",
        10: "Octubre",
        11: "Noviembre",
        12: "Diciembre",
    }

    return month_dict[value]


@register.filter
def hours_format(value):
    hours = int(value)
    mins = value - hours
    if mins > 0:
        return f"{hours}:{int(mins*60)}"
    return f"{hours}:00"
