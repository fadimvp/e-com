from django.contrib import admin

# Register your models here.
from .models import Product,Variotion,ProductImage,Category,ProductFeatured
class CategoryInLine(admin.TabularInline):
    model = ProductFeatured
    extra = 0

class ImageInLine(admin.TabularInline):
    model = ProductImage
    extra = 0

class VariationInLine(admin.TabularInline):
    model = Variotion
    extra = 0
class ProductAdmin(admin.ModelAdmin):
    list_display = ['__unicode__','price']
    inlines =[ VariationInLine,ImageInLine,CategoryInLine,
               ]
    class Meta:
        model=Product

admin.site.register(Product,ProductAdmin)
admin.site.register(Variotion)
admin.site.register(ProductImage)
admin.site.register(Category)
admin.site.register(ProductFeatured)