from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth import get_user_model
from .models import RequestModel
from location_field.forms.plain import PlainLocationField, LocationWidget
from .models import QonunBuzilishOptions
User = get_user_model()

class RequestForm(forms.Form):

    taxminiy_qonun_buzilishi = forms.ChoiceField(
        choices=QonunBuzilishOptions.choices, 
        initial=QonunBuzilishOptions.BOSHQA,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'style': 'margin-bottom: 20px;',
            }
        ),
        label="Taxminiy qonun buzilishi",
    )

    text_context = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': "So'rovnoma izohi", 
            'style': 'height: 150px; margin-bottom: 20px;',
            'class':'form-control',
            }),
        label="So'rovnoma izohi",
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
    location = PlainLocationField( 
        based_fields=['city'], 
        zoom=15,
        initial="38.8612, 65.7847",
    )
    send_hokimiyat = forms.BooleanField(
        label="Hokimiyatga yuborish",
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                "style":"margin-top: 20px;"
            }
        )
    )
    send_qurilish = forms.BooleanField(
        label="Qurilish bo'limiga yuborish",
        required=False
    ) 
    send_kadastr = forms.BooleanField(
        label="Kadastr agentligiga yuborish",
        required=False

    )


    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data['send_hokimiyat'] \
            and not cleaned_data['send_qurilish'] \
                and not cleaned_data['send_kadastr']:
            raise ValidationError("Kamida bitta qabul qiluvchi kiritilishi shart!")

        return super().clean()