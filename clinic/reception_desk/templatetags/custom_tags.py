from django import template
from django.utils.safestring import mark_safe
import json


register = template.Library()


@register.filter(is_safe=True)
def js_safe(obj):
    return mark_safe(json.dumps(str(obj)))


@register.filter
def js_not_safe(obj):
    return json.dumps(str(obj))


@register.filter
def get_date(date):
    return json.dumps(date.strftime("%Y-%m-%d"))


@register.filter
def get_hour(arrived):
    return json.dumps(int(arrived.hour))


@register.filter
def get_minute(arrived):
    return json.dumps(int(arrived.minute))

@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        if k != "from_date":
            del d[k]
    return d.urlencode()
