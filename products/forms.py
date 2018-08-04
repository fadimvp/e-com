from django import forms
from django.forms.models import modelformset_factory
from .models import Variotion

class VariotionInventoryForm (forms.ModelForm):
    class Meta:
        model =Variotion
        fields = [
            "title",
            "price",
            "sale_price",
            "inventory",
            "active"
        ]
VariotionInventoryFormSet =modelformset_factory(Variotion,form=VariotionInventoryForm,extra=0)
