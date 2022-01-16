from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.core.exceptions import ValidationError
from django.conf import settings


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