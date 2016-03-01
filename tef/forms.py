from django import forms


class SearchForm(forms.Form):
    query = forms.RegexField(
        '^[ACTGactg]+$',
        label='DNA Sequence'
    )
    start_loc = forms.IntegerField(
        label='Start Location',
        min_value=0
    )
    end_loc = forms.IntegerField(label='End Location')
