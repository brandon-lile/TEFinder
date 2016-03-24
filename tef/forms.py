from django import forms
import re


class SearchForm(forms.Form):
    query = forms.RegexField(
        r'>(.)*\n([ACTGactg\r\n]*)$',
        label='FASTA Sequence',
        widget=forms.Textarea
    )
    threshold = forms.IntegerField(
        label='Threshold',
        min_value=1,
        initial=60
    )
    distance = forms.IntegerField(
        label='Distance',
        min_value=1,
        initial=50
    )

    def clean_query(self):
        data = self.cleaned_data['query']
        data = re.sub(r'>(.)*\n', '', data)
        data = re.sub(r'(\r\n)*', '', data)
        return data.upper()

    def clean(self):
        cleaned_data = super(SearchForm, self).clean()
