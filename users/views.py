from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView

from .forms import SignUpForm, LoginForm, KitchenSignupForm
from kitchen.models import Kitchen


class KitchenSignupView(CreateView):
    model = User
    form_class = KitchenSignupForm
    template_name = "register2.html"

    def get_context_data(self, **kwargs):
        kwargs["user_type"] = "kitchen"
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('kitchen:kitchen_create', user.id)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            # user.profile.email = form.cleaned_data.get('email')
            # user.profile.security_question1 = form.cleaned_data.get('security_question1')
            # user.profile.security_question2 = form.cleaned_data.get('security_question2')
            # user.profile.answer_question1 = form.cleaned_data.get('answer_question1')
            # user.profile.answer_question2 = form.cleaned_data.get('answer_question2')

            user.sq1 = form.cleaned_data.get('security_question1')
            user.sq2 = form.cleaned_data.get('security_question2')
            user.aq1 = form.cleaned_data.get('answer_question1')
            user.aq2 = form.cleaned_data.get('answer_question2')

            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('/kitchen')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def user_detail(request):
    # if request.user.is_kitchen:
    #     return redirect('kitchen:kitchen_detail', pk=request.user.id)
    # else:
        return render(request, 'user_detail.html')

def home(request):
    kitchens = Kitchen.objects.all()
    return render(request, "kitchen/kitchen_list.html", {"kitchens": kitchens})

def register(request):
    return render(request, 'register.html')
