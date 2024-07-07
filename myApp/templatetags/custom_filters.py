from django import template

register = template.Library()

@register.filter(name='custom_slice')
def custom_slice(file_name):
    if len(file_name) > 3 and file_name[2] == '_' and file_name[:2].isdigit():
        return file_name[3:-4]
    else:
        return file_name[:-4]
