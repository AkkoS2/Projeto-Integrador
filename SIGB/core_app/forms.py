from django import forms
from .models import Bombeiro


class FormBombeiro(forms.ModelForm):

    class Meta:
        model = Bombeiro
        fields = '__all__'
        widgets = {
            'nome_completo': forms.TextInput(attrs={'class': 'form-control'}),
            'patente': forms.Select(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'data_ingresso': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'})
        }