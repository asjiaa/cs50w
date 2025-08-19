import calendar
from datetime import date
from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(
        label="Topic", 
        max_length=200,
        widget=forms.TextInput(attrs={
            "id": "search-bar",
            "placeholder": "Search Topic",
            "class": "search-input"
        })
    )

    # Choice field of years from current year
    YEARS = [(y, y) for y in range(date.today().year, 1999, -1)]

    # Choice field of months
    MONTHS = [(m, calendar.month_name[m]) for m in range(1, 13)]

    start_year = forms.ChoiceField(
        choices=YEARS, 
        label="From",
        widget=forms.Select(attrs={"class": "custom-select"})
    )
    start_month = forms.ChoiceField(
        choices=MONTHS, 
        initial=date.today().month,
        widget=forms.Select(attrs={"class": "custom-select"})
    )

    end_year = forms.ChoiceField(
        choices=YEARS,
        label="To",
        widget=forms.Select(attrs={"class": "custom-select"})
    )
    end_month = forms.ChoiceField(
        choices=MONTHS,
        initial=date.today().month,
        widget=forms.Select(attrs={"class": "custom-select"})
    )