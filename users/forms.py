from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import User
from django.db import transaction

from kitchen.models import Profile

class KitchenSignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "email", "password1", "password2", ]

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_kitchen = True
        user.is_customer = False
        user.is_active = False
        user.save()
        return user

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=254)

    CHOICES1 = (
        ('What is your favorite color?', 'What is your favorite color?'),
        ('What is your mother name?', 'What is your mother name?')
    )
    CHOICES2 = (
        ('Where is your hometown?', 'Where is your hometown?'),
        ('What is your father name?', 'What is your father name?')
    )

    security_question1 = forms.ChoiceField(choices=CHOICES1,label='Security Question 1')
    answer_question1 = forms.CharField(max_length=255,label='Answer')
    security_question2 = forms.ChoiceField(choices=CHOICES2,label='Security Question 2')
    answer_question2 = forms.CharField(max_length=255,label='Answer')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)

class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=200)
    password = forms.CharField(label="Password", max_length=200, widget=forms.PasswordInput)
