from django import template

register = template.Library()

@register.inclusion_tag('components/search_box.html')
def search_box_recipes(action=None, placeholder=None, button_text=None):
    """
    Render a reusable search box component
    """

    if action is None:
        action = "url 'search'"

    return {
        'action': action,
        'placeholder': placeholder,
        'button_text': button_text
    }