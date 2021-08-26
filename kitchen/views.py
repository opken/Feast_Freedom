from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import User
from django.forms import ModelForm
from django import forms

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from .models import Kitchen, Item, Day
from .forms import KitchenForm, ItemForm, ItemFormSet, KitchenCreateForm


def kitchen_detail(request, pk):
    kitchen = get_object_or_404(Kitchen, pk=pk)
    menu = Item.objects.filter(kitchen=kitchen.user_id)
    lst = []
    for item in menu:
        lst.append(item)

    return render(request, 'kitchen/kitchen_detail.html', {'kitchen': kitchen, 'menu': lst})


def menu_detail(request, pk):
    kitchen = get_object_or_404(Kitchen, pk=pk)
    menu = Item.objects.filter(kitchen=kitchen.user_id)
    lst = []
    for item in menu:
        lst.append(item)

    return render(request, 'menu/menu_detail.html', {'kitchen': kitchen, 'menu': lst})


def create_kitchen(request, user_id):
    if request.method == "POST":
        form = KitchenCreateForm(request.POST, request.FILES)
        formset = ItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            user = User.objects.get(pk=user_id)
            kitchen = form.save()
            kitchen.user = user
            kitchen.user.is_active = True
            kitchen.save()
            kitchen.days.add(*form.cleaned_data.get("days"))
            kitchen.save()
            user.save()
            for f in formset:
                item = f.save(commit=False)
                item.kitchen = kitchen
                item.save()
            messages.success(request, f'Your Kitchen has been been created!')
            return redirect("kitchen:kitchen_list")
    else:
        formset = ItemFormSet(queryset=Item.objects.none())
        form = KitchenCreateForm()
    return render(request, "kitchen/kitchen_create.html", {"user_id": user_id, "form": form, "formset": formset})

class MenuAddItem(LoginRequiredMixin, CreateView):
    model = Item
    form_class = ItemForm
    template_name = 'menu/menu_add_item.html'
    login_url = 'login'

    def create_form(self, *args, **kwargs):
        form = super(MenuAddItem, self).create_form(*args, **kwargs)
        form.instance.user = self.request.user
        form.instance.kitchen_id = self.kwargs['pk']
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.kitchen = get_object_or_404(Kitchen, pk=self.kwargs['pk'])
        return super(MenuAddItem, self).form_valid(form)

    def get_success_url(self):
        kitchen_id = self.kwargs['pk']
        return reverse_lazy('kitchen:menu_detail', kwargs={'pk': kitchen_id})


class MenuUpdateItem(UpdateView):
    model = Item
    form_class = ItemForm
    template_name = 'menu/menu_update_item.html'

    def get_success_url(self):
        item_id = self.kwargs['pk']
        item = get_object_or_404(Item, pk=item_id)

        return reverse_lazy('kitchen:menu_detail', kwargs={'pk': item.kitchen_id})


class MenuDeleteItem(DeleteView):
    model = Item
    template_name = 'menu/menu_delete_item.html'

    def get_success_url(self):
        item_id = self.kwargs['pk']
        item = get_object_or_404(Item, pk=item_id)

        return reverse_lazy('kitchen:menu_detail', kwargs={'pk': item.kitchen_id})
