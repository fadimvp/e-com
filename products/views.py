from django import http
from django.contrib import messages
from django.db.models import Q
from django.http import Http404
from django.utils import translation
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import render,get_object_or_404,redirect
from django.conf import settings





# Create your views here.
from .forms import VariotionInventoryFormSet
from .mixins import StaffRequiredMixin,LoginRuquirdMixin
from .models import Product,Variotion,Category


class CategoryListView(ListView):
    model = Category
    queryset = Category.objects.all()
    template_name = "products/product_list.html"


class CategoryDetailview(DetailView):

    model = Category
    def get_context_data(self,*args, **kwargs):
        context = super(CategoryDetailview,self).get_context_data(*args ,**kwargs)
        obj = self.get_object()
        product_set = obj.product_set.all()
        default_products = obj.default_category.all()
        products = (product_set | default_products)
        context["products"] = products
        return context

class VariationListView(StaffRequiredMixin,ListView):
    model = Variotion
    queryset = Variotion.objects.all()
    def get_context_data(self,*args, **kwargs):
        context =super(VariationListView,self).get_context_data(*args,**kwargs)
        context["formset"]= VariotionInventoryFormSet(queryset=self.get_queryset())

        return context
    def get_queryset(self,*args,**kwargs):
        product_pk =self.kwargs.get("pk")
        if product_pk:
            product = get_object_or_404(Product,pk=product_pk)
            queryset =Variotion.objects.filter(Product=product)
        return queryset
    def post(self,request,*args,**kwargs):
        formset =VariotionInventoryFormSet(request.POST, request.FILES)
        if formset.is_valid():
            formset.save(commit=False)
            for form in formset :
                new_item =form.save(commit=False)
                if new_item.title:
                    product_pk = self.kwargs.get("pk")
                    product =get_object_or_404(Product,pk= product_pk)
                    new_item.Product =product
                    new_item.save()
            messages.success(request,"your and pricing has been update ")
            return redirect("pro")
        raise Http404

class ProductListView(ListView):
    model = Product
    queryset = Product.objects.all()
    def get_context_data(self,*args, **kwargs):
        context =super(ProductListView,self).get_context_data(*args,**kwargs)

        return context
    def get_queryset(self,*args,**kwargs):
        qs= super(ProductListView,self).get_queryset(*args,**kwargs)
        query= self.request.GET.get("q")
        if query :
            qs=self.model.objects.filter(
                Q(title__icontains=query)|
                Q(description__icontains=query)
            )

        return qs
import random
class ProductDetalView(DetailView):
    model = Product
    def get_context_data(self,*args,**kwargs):
        context = super(ProductDetalView, self).get_context_data(*args,**kwargs)
        instance = self.get_object()
        context['related']= sorted(Product.objects.get_related(instance)[:4], key=lambda x: random.random())
        return context


def product_detail_view_func(request,id ):
    product_instance =get_object_or_404(Product,id=id)
    try:

        product_instance = Product.objects.get(id=id)
    except Product.DoesNotExist:
        raise Http404
    except:
        raise  Http404
    template ="products/product_detail.html"
    context ={
        "object":product_instance
    }
    return render(request,template,context)

def change_language(request):
    # current_language =translation.get_language()
    # if current_language =="ar":
    #     lang_code = "en"
    # else:
    #     lang_code ="ar"
    lang_code =request.GET.get('lang_code')
    response =http.HttpResponseRedirect(request.GET.get("return_url"))
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME,lang_code)
    translation.activate(lang_code)
    return response

