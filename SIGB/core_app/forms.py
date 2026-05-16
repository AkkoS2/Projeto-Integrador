from django import forms
from .models import Bombeiro, Escala, EscalaBombeiro, Manutencao


class EscalaForm(forms.ModelForm):

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


class ManutencaoForm(forms.ModelForm):
    
    class Meta:
        model = Manutencao
        fields = ['data_inicio', 'data_fim', 'tipo', 'status', 'descricao']

        widgets = {
            'data_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form_control'}),
            'data_fim': forms.DateInput(attrs={'type' : 'date', 'class': 'form-control'}),
            'tipo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Exemplo: Elétrica, Manutenção, etc...'}),
            'status': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Exemplo: Em Andanmento, Finalizado, etc...'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }


class BombeiroForm(forms.ModelForm):

    class Meta:
        model = Bombeiro
        fields = '__all__'
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_ingresso': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'nome_completo': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'tipo_sanguineo': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.TextInput(attrs={'class': 'form-control'}),
            'patente': forms.Select(attrs={'class': 'form-control'}),
            'perfil': forms.Select(attrs={'class': 'form-control'})
        }