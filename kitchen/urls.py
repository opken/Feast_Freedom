from django.urls import path, reverse_lazy
from django.views.generic import ListView, DeleteView, UpdateView
from .models import Kitchen, Item
from .forms import KitchenForm, ItemForm, KitchenCreateForm
from . import views
from .views import \
    MenuAddItem, MenuUpdateItem, MenuDeleteItem \
# KitchenCreate,
from users.models import User

app_name = 'kitchen'

urlpatterns = [
    path('', ListView.as_view(
        queryset=Kitchen.objects.all(),
        context_object_name='kitchen_list',
        template_name='kitchen/kitchen_list.html'),
        name='kitchen_list',
    ),
    path('<int:pk>/', views.kitchen_detail, name='kitchen_detail'),

    # path('create/', KitchenCreate.as_view(), name='kitchen_create'),

    path("<int:user_id>/create", views.create_kitchen, name="kitchen_create"),

    path('<int:pk>/delete/', DeleteView.as_view(
        model=Kitchen,
        template_name='kitchen/kitchen_delete.html',
        success_url=reverse_lazy('kitchen:kitchen_list')),
        name='kitchen_delete',
    ),

    path('<int:pk>/update/', UpdateView.as_view(
        model=Kitchen,
        template_name='kitchen/kitchen_update.html',
        form_class=KitchenCreateForm),
        name='kitchen_update'
    ),

    path('<int:pk>/menu/', views.menu_detail, name='menu_detail'),
    path('<int:pk>/menu/add', MenuAddItem.as_view(), name='menu_add_item'),
    path('item/<int:pk>/update/', MenuUpdateItem.as_view(), name='menu_update_item'),
    path('item/<int:pk>/delete/', MenuDeleteItem.as_view(), name='menu_delete_item'),
]