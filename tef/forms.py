from django import forms


class SearchForm(forms.Form):
    query = forms.RegexField(
        '^[ACTGactg]+$',
        label='DNA Sequence'
    )
    start_loc = forms.IntegerField(
        label='Start Location',
        min_value=0,
        initial=0
    )
    end_loc = forms.IntegerField(
        label='End Location',
        min_value=0,
        initial=0
    )
    threshold = forms.IntegerField(
        label='Threshold',
        min_value=0,
        initial=3
    )

    def clean_query(self):
        data = self.cleaned_data['query']
        return data.upper()
