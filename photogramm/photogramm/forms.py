from django import forms
from photos.models import Photo, Comment
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class PhotoForm(forms.Form):
    image = forms.FileField(label='Изображение', required=True)
    captions = forms.CharField(widget=forms.Textarea, label='Описание', required=True)


class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image', 'caption']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    username = forms.CharField(required=False)
    age = forms.IntegerField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'age']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Этот адрес электронной почты уже занят.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Пароли не совпадают.")

        if len(password) < 8:
            raise forms.ValidationError("Пароль должен содержать не менее 8 символов.")


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, label='Имя пользователя')
    password = forms.CharField(widget=forms.PasswordInput, required=True, label='Пароль')
