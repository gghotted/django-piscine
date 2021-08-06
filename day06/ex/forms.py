from django import forms
from django.contrib import auth
from .models import User, Tip

# 참고 https://jinmay.github.io/2019/11/13/django/django-form-is-valid-mechanism-brief/
class SignupForm(forms.ModelForm):
    password = forms.CharField(max_length=20, widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(max_length=20, widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ['username']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            self.add_error('username', 'Already exist username')
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            self.add_error('confirm_password', "Password != Confirm password")

        return cleaned_data

    def save(self, commit=True):
        instance = self.Meta.model()
        instance.username = self.cleaned_data.get('username')
        instance.set_password(self.cleaned_data.get('password'))
        if commit:
            instance.save()
        return instance


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if not User.objects.filter(username=username).exists():
            self.add_error('username', 'Dose not exist username')
            return cleaned_data

        if not User.objects.get(username=username).check_password(password):
            self.add_error('password', 'Dose not matched')

        return cleaned_data


class TipForm(forms.ModelForm):
    class Meta:
        model = Tip
        fields = ['content']
