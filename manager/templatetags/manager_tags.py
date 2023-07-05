from django import template

register = template.Library()


@register.inclusion_tag("snipets/active_icon.html")
def active_icon(active):
    return {"active": active}


@register.inclusion_tag("snipets/paginator.html")
def paginator(page_obj):
    return {"page_obj": page_obj}
