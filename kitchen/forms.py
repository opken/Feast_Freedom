from django import forms
from django.forms import ModelForm

from django.forms import modelformset_factory

from .models import Kitchen, Item, Day

class KitchenCreateForm(ModelForm):
    days = forms.ModelMultipleChoiceField(
        queryset=Day.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    class Meta:
        model = Kitchen
        fields = ["name", "start_time", "end_time", "days", "image",]
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'})
        }
        labels = {
            "name": "Kitchen Name",
            "days": "Open Days"
        }


    def save(self, commit=True):
        kitchen = super().save(commit=False)
        return kitchen

ItemFormSet = modelformset_factory(Item, fields=('name', 'vegan', 'price'), extra=1)

class KitchenForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Kitchen
        exclude = ('user',)

    def clean(self):
        cleaned_data = super(KitchenForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if password != confirm_password:
            self.add_error('confirm_password', "Password not match")

        if start_time >= end_time:
            self.add_error('end_time', 'End Time has to be later than Start Time')
        return cleaned_data


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ('kitchen', 'user')
