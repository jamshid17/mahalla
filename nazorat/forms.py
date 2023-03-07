from django import forms
from django.core.exceptions import ValidationError

class RangeForm(forms.Form):
    start_range = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type':'date',
                'class':'form-control date-ranger',
                'min':'2023-01-01',
                'max':'2030-12-31'
            }
        ),
        label='Boshlanish sanasi'
    )
    end_range = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type':'date',
                'class':'form-control date-ranger',
                'min':'2023-01-01',
                'max':'2030-12-31'
            }
        ),
        label='Tugash sanasi'
    )
    
    def clean(self):
        cleaned_data = super().clean()
        
        if cleaned_data['start_range'] > cleaned_data['end_range']:
            raise ValidationError(
                "Boshlanish sanasi tugash sanasidan oldinroq kelgan bo'lishi shart!"
                )

        return super().clean()