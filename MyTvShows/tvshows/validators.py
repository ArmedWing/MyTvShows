from django.core.exceptions import ValidationError


def check_name_capital_letter(value):
    if not value[0].isupper():
        raise ValidationError('Your name must start with a capital letter!')
