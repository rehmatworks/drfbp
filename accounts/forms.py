from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Token
from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.core import validators


class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(required=True)
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            user = User.objects.filter(email=email).first()
            if not user:
                raise ValidationError('An active account cannot be found for this email.')
            
            if user.tokens.count() >= int(settings.MAX_PENDING_USER_TOKENS):
                raise ValidationError('Too many password reset requests received. Please wait before trying again.')
            
        return email
    
    def save(self):
        email = self.cleaned_data.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            return user.tokens.create()
        return None
    

class PasswordUpdateForm(forms.Form):
    token = forms.CharField(max_length=255)
    password = forms.CharField(validators=[validate_password])
    
    def clean_token(self):
        tok = self.cleaned_data.get('token')
        if tok:
            user = User.objects.filter(tokens__token=tok).first()
            if not user or not user.is_token_valid(tok):
                raise ValidationError('The token is either invalid or expired.')
        return tok
    
    def save(self):
        password = self.cleaned_data.get('password')
        tok = self.cleaned_data.get('token')
        user = User.objects.filter(tokens__token=tok).first()
        if user and user.is_token_valid(tok):
            user.set_password(password)
            user.save()
            Token.objects.filter(user=user, token=tok).delete()
            return True
        return False