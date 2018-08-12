from django.contrib import admin
from .models import UserCheckout,UserAddress,Order
from .forms import AddressForm,UserAddressForm,UserOrderForm

# Register your models here.
class UserForm(admin.ModelAdmin):
    list_display = ['status','cart','user']
    form = UserOrderForm

admin.site.register(UserCheckout)
admin.site.register(UserAddress)

admin.site.register(Order,UserForm)

