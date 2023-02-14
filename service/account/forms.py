from .models import User
from django import forms
from django.contrib.auth.forms import AuthenticationForm

class RegistrationForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ('phone', 'password', 'first_name', 'patronymic', 'last_name')
        widgets = {
            'first_name': forms.TextInput(attrs={'title': 'Имя', 'placeholder': 'Иван', 'class': 'first_name_field input-text', 'required': 'True'}),
            'patronymic': forms.TextInput(attrs={'title': 'Отчество','placeholder': 'Иванович', 'class': 'patronymic_field input-text', 'required': 'True'}),
            'last_name': forms.TextInput(attrs={'title': 'Фамилия','placeholder': 'Иванов', 'class': 'last_name_field input-text'}),
            'phone': forms.TextInput(attrs={'title': 'Номер телефона','placeholder': '+79140000000', 'class': 'phone_field input-text', 'required': 'True'}),
            # 'snils': forms.TextInput(attrs={'title': 'СНИЛС','placeholder': '00000000000', 'class': 'snils_field input-text', 'required': 'True'}),
            'password': forms.PasswordInput(attrs={'title': 'Пароль','placeholder': 'Пароль', 'class': 'password_field input-text', 'required' : 'True', 'min_length' : '6'}),
        }


# class RegistrationForm(forms.Form):
#     first_name = forms.CharField(widget=forms.TextInput(attrs={'name': 'Имя', 'placeholder': 'Иван', 'class': 'first_name_field input-text', 'required': 'True'}))
#     patronymic = forms.CharField(widget=forms.TextInput(attrs={'name': 'Отчество','placeholder': 'Иванович', 'class': 'patronymic_field input-text', 'required': 'True'}))
#     last_name = forms.CharField(widget=forms.TextInput(attrs={'name': 'Фамилия','placeholder': 'Иванов', 'class': 'last_name_field input-text'}))
#     phone = forms.CharField(widget=forms.TextInput(attrs={'name': 'Номер телефона','placeholder': '+79140000000', 'class': 'phone_field input-text', 'required': 'True'}))
#     # 'snils': forms.TextInput(attrs={'title': 'СНИЛС','placeholder': '00000000000', 'class': 'snils_field input-text', 'required': 'True'}),
#     password = forms.CharField(widget=forms.TextInput(attrs={'name': 'Пароль','placeholder': 'Пароль', 'class': 'password_field input-text', 'required' : 'True', 'min_length' : '6'}))


class LoginForm(AuthenticationForm):
    username = forms.TextInput(attrs={'title': 'Телефон', 'placeholder': '+79140000000', 'class': 'login_field input-text', 'required' : 'True'})
    password = forms.PasswordInput(attrs={'title': 'Пароль', 'placeholder': 'Пароль', 'class': 'password_field input-text', 'required' : 'True'})

