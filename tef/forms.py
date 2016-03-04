from django import forms
import re


class SearchForm(forms.Form):
    query = forms.RegexField(
        r'>(.)*\n([ACTGactg\r\n]*)$',
        label='FASTA Sequence',
        widget=forms.Textarea
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
        min_value=1,
        initial=3
    )

    def clean_query(self):
        data = self.cleaned_data['query']
        data = re.sub(r'>(.)*\n', '', data)
        data = re.sub(r'(\r\n)*', '', data)
        return data.upper()

    def clean_end_loc(self):
        loc = self.cleaned_data['end_loc']
        if 'query' in self.cleaned_data:
            size = len(self.cleaned_data['query'])
            if loc == 0 or loc > size - 1:
                return size - 1
            else:
                return loc
        else:
            # Doesn't matter
            return loc

    def clean(self):
        cleaned_data = super(SearchForm, self).clean()
        start_loc = cleaned_data.get("start_loc")
        end_loc = cleaned_data.get("end_loc")

        # Will catch if start_loc > len(query)
        if start_loc > end_loc:
            self.add_error('end_loc', 'End location must be greater than start location')
