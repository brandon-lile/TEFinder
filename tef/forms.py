from django import forms
from django.forms import Textarea
from django.core.validators import RegexValidator


class DNAField(Textarea):
    default_validators = [
        RegexValidator(
            '^[ACTGactg]*$',
            'Must be a valid DNA sequence'
        )
    ]


class SearchForm(forms.Form):
    query = DNAField()
    start_loc = forms.NumberInput(label='Start Location')
    end_loc = forms.NumberInput(label='End Location')
