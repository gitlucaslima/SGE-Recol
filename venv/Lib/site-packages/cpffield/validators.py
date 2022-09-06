import re
from django.utils.translation import ugettext_lazy as _
from django.forms import ValidationError

default_error_messages = {
    'invalid': _('Número de CPF inválido'),
    'max-digits': _('CPF deve ter 11 digitos')
}

cpf_digits_re = re.compile(r'^(\d{3})\.(\d{3})\.(\d{3})-(\d{2})$')


def validate_cpf(value):
    original_value = value[:]
    if not value.isdigit():
        cpf = cpf_digits_re.search(value)
        if cpf:
            value = ''.join(cpf.groups())
        else:
            raise ValidationError(default_error_messages['invalid'], 'format')

    if len(value) != 11:
        raise ValidationError(default_error_messages['max-digits'], 'length')

    return original_value
