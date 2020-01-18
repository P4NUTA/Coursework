from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label="Логин ", max_length=100)
    password = forms.CharField(label="Пароль ", max_length=100)

class AddUser (forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50)
    Function = forms.TypedChoiceField()

