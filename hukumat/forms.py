from django import forms
from .models import Response


class ResponseForm(forms.ModelForm):
    
    class Meta:
        model = Response
        fields = [
            'buyruq',
            'extra_file',
            'is_certified',
        ]
        widgets = {
            'buyruq' : forms.ClearableFileInput(attrs={
                'style': 'margin-bottom: 20px;',
                'class':'form-control'
                },
            ),
            'extra_file' : forms.ClearableFileInput(attrs={
                'style': 'margin-bottom: 20px;',
                'class':'form-control'
                }
            ),
            # 'is_certified' : forms.CheckboxInput(
            #     attrs={
            #         'style': 'margin-bottom: 20px;'
            #     }
            # )
        }
        labels = {
            "extra_file": "Qo'shimcha hujjat",
            "is_certified" : "Tasdiqlangan*"
        }