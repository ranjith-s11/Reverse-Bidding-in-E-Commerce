from django import forms
from.models import *
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User


class SignupForm(UserCreationForm):
	mob_no=forms.CharField(widget=forms.TextInput(attrs={'type':'number'}))
	address=forms.CharField(max_length=50,required=True)
	class Meta:
		model=User
		fields=('first_name','last_name','mob_no','address','email','username','password1','password2')

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('comment' , 'rating')
        
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        
        