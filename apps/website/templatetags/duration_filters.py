from django import template

register = template.Library()

@register.filter
def minutes_to_hours(minutes):
    """
    Convertit des minutes en :
    - "45 min"
    - "1 h"
    - "1 h 30"
    """
    try:
        minutes = int(minutes)
    except (TypeError, ValueError):
        return ""

    if minutes < 60:
        return f"{minutes} min"

    hours = minutes // 60
    remaining = minutes % 60
    if remaining == 0:
        return f"{hours} h"
    return f"{hours} h {remaining} min"

