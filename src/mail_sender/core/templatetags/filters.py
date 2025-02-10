from django import template

register = template.Library()


@register.filter(name="add_class")
def add_class(value, classes):
    return value.as_widget(attrs={"class": classes})
