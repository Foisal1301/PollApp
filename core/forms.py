from django.forms import ModelForm,EmailField
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm,UserChangeForm
from .models import Topic,Choice
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
	email = EmailField()
	class Meta:
		model = User
		fields = ["username",'email',"password1","password2"]

class AddPollForm(ModelForm):
    class Meta:
        model = Topic
        fields = ('name',)

class PrivacyForm(UserChangeForm):
	class Meta:
		model = User
		fields = ("username",)

class PasswordChangingForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ('old_password','new_password1','new_password2',)