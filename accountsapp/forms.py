from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ValidationError
from django.forms import extras

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',)


    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError(u'Username "%s" is already in use.' % username)
        return username

    def clean(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        # validation for email and username goes here later
        return self.cleaned_data

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class AuthenticationForm(AuthenticationForm):
        error_css_class = "login_style3"
        error_messages = {
        'invalid_username': _("Invalid Username"),
        'invalid_password': _("Invalid Password"),
        'inactive': _("This account is inactive."),
        'required': _("This field is required."),
        }

        def clean_username(self):
            username = self.data['username']
            try:
                username = User.objects.get(username=username).username
            except ObjectDoesNotExist:
                raise ValidationError(
                self.error_messages['invalid_username'],
                code='invalid_login',
                params={'username':self.username_field.verbose_name},
            )
            return username
