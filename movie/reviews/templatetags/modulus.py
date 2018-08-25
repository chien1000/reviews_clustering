from django import template

register = template.Library()

def modulus(value, arg):
    """compute value % arg"""
    return value % arg

register.filter('modulus', modulus)