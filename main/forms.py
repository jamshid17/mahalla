from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth import get_user_model
from .models import RequestModel


User = get_user_model()

class RequestForm(forms.Form):
    text_context = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': "So'rovnoma mazmuni", 
            'style': 'height: 150px; margin-bottom: 20px;',
            'class':'form-control',
            }),
        label="So'rovnoma mazmuni",
        )
    address = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Manzil', 
            'style': 'height: 150px; margin-bottom: 10px;',
            'class':'form-control',
            }),
        label="Manzil",
        )
    image = forms.ImageField(
        widget=forms.ClearableFileInput(
            attrs={
                'style': 'margin-bottom: 20px;',
                'class':'form-control', 
            }
        ),
        label='Rasm'
    )
    send_hokimiyat = forms.BooleanField(
        label="Hokimiyatga yuborish",
        required=False
    )
    send_qurilish = forms.BooleanField(
        label="Qurilishga yuborish",
        required=False
    ) 
    send_kadastr = forms.BooleanField(
        label="Kadastrga yuborish",
        required=False

    )


    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data['send_hokimiyat'] \
            and not cleaned_data['send_qurilish'] \
                and not cleaned_data['send_kadastr']:
            raise ValidationError("Kamida bitta qabul qiluvchi kiritilishi shart!")

        return super().clean()