from django import template


register = template.Library()

@register.filter()
def blankstate(seq, num):
    """
    Backfill sequence with None if needed.
    """
    return seq + [None] * max(num - len(seq), 0)
