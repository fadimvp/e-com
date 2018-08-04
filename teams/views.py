from django.shortcuts import render

from .forms import FormSignUp
from .models import Signup
from products.models import ProductFeatured,Product
# Create your views here.
def form (request):
    contxt ={

    }
    return render(request,'signup.html',contxt)


def home (request):
    title = "welcome "
    featured_image = ProductFeatured.objects.filter(active=True).order_by("?").first()
    products = Product.objects.all().order_by("?")[:100]
    form = FormSignUp(request.POST or None)

    contxt ={
        "title": title,
        "products": products,
        'form': form,
        "featured_image": featured_image,


    }
    if form.is_valid():
        instance=form.save(commit=False)
        full_name =form.cleaned_data.get("full_name")
        if not full_name:
            instance.full_name=full_name
            instance.save()



        contxt ={
        "title":'thank you',


    }
    return render(request,'home.html',contxt)
