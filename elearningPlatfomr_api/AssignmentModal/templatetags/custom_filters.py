# custom_filters.py

from django import template

register = template.Library()

@register.filter
def get_item(dictionary_list, key):
    for dictionary in dictionary_list:
        if dictionary.get('assignment_id') == key:
            return dictionary.get('student_has_submission')
    return None
