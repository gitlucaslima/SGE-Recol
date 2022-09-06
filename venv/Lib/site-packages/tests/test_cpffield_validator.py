from django.test import SimpleTestCase

from cpffield.forms import MyModelForm


class CPFFieldValidatorsTests(SimpleTestCase):
    def test_has_fields(self):
        """Form must have 4 fields"""
        form = MyModelForm()
        expected = ['cpf']
        self.assertSequenceEqual(expected, list(form.fields))

    def test_valid_data(self):
        form = self.make_validated_form(cpf="20179291823")
        self.assertTrue(form.is_valid())

    def test_cpf_is_digit(self):
        """CPF must only accept digit"""
        form = self.make_validated_form(cpf='abc12345678')
        self.assertFormErrorCode(form, 'cpf', 'format')

    def test_cpf_has_11_digits(self):
        """CPF must have 11 digits"""
        form = self.make_validated_form(cpf='1234')
        self.assertFormErrorCode(form, 'cpf', 'length')

    def assertFormErrorCode(self, form, field, code):
        errors = form.errors.as_data()
        errors_list = errors[field]
        exception = errors_list[0]
        self.assertEqual(code, exception.code)

    def make_validated_form(self, **kwargs):
        valid = dict(cpf='12345678901')
        data = dict(valid, **kwargs)
        form = MyModelForm(data)
        form.is_valid()
        return form

