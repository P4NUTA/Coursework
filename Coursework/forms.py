from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label="Логин ", max_length=100)
    password = forms.CharField(label="Пароль ", max_length=100)

class AddUser (forms.Form):
    Name = forms.CharField(max_length=50)
    Login = forms.CharField(max_length=50)
    Password = forms.CharField(max_length=50)
    Function = forms.TypedChoiceField()
