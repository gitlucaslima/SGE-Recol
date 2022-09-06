from django.db import models
from cpffield.validators import validate_cpf


class CPFField(models.CharField):
    default_validators = [validate_cpf]

    def __init__(self, *args, **kwargs):
        super(CPFField, self).__init__(*args, **kwargs)


