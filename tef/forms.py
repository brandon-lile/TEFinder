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

    def clean_end_loc(self):
        loc = self.cleaned_data['end_loc']
        size = len(self.cleaned_data['query'])
        if loc == 0:
            return size - 1
        else:
            return loc

    def clean(self):
        cleaned_data = super(SearchForm, self).clean()
        start_loc = cleaned_data.get("start_loc")
        end_loc = cleaned_data.get("end_loc")

        # Will catch if start_loc > len(query)
        if start_loc > end_loc:
            self.add_error('end_loc', 'End location must be greater than start location')
