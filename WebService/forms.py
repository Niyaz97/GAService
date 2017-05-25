from django import forms
from .models import Chart


class AddChart(forms.ModelForm):

    class Meta:
        model = Chart
        fields = ('viewId', 'metric', 'startDate', 'endDate', 'width', 'height')