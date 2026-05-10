from django import forms
from .models import Bombeiro, Escala, EscalaBombeiro


class FormEscala(forms.ModelForm):

    bombeiros = forms.ModelMultipleChoiceField(
        queryset=Bombeiro.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control', 'style': 'height: 150px;'}),
        help_text='Mantenha CTRL pressionado pra selecionar mais de um.'
    )


    class Meta:
        model = Escala
        fields = ['nome', 'data_inicio', 'data_fim', 'descricao']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form_control'}),
            'data_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_fim': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }
