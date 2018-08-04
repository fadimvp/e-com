
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.utils.safestring import  mark_safe
from django.utils.text import slugify

# Create your models here.
class ProductQuerySet(models.query.QuerySet):
    def acvtive(self):
        return self.filter(active=True)
class ProductManger(models.Manager):
    def get_queryset(self):

        return ProductQuerySet(self.model,using=self._db)
    def all(self,*args,**kwargs):
        return self.get_queryset().acvtive()
    def get_related(self,instance):
        products_one =self.get_queryset().filter(categories__in=instance.categories.all())
        products_two =self.get_queryset().filter(default = instance.default )
        qs = (products_one | products_two).exclude(id=instance.id).distinct()
        return qs

class Product(models.Model):

    title = models.CharField(max_length=120)
    description = models.TextField(blank=True,null=True)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    active = models.BooleanField(default=True)
    categories = models.ManyToManyField('Category',blank=True)
    default = models.ForeignKey('Category',related_name='default_category',null=True,blank=True)
    objects = ProductManger()
    class Meta:
        ordering = ["-title"]


    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("product_detail",kwargs={"pk":self.pk })
    def get_image_url(self):
        img = self.productimage_set.first()
        if img :
            return img.image.url
        return img


class Variotion (models.Model):
    Product = models.ForeignKey(Product)
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    sale_price = models.DecimalField(decimal_places=2, max_digits=20,null=True,blank=True)
    active = models.BooleanField(default=True)
    inventory = models.IntegerField(null=True,blank=True)

    def __unicode__(self):
        return self.title

    def get_price(self):
        if self.sale_price is not None:
            return self.sale_price
        else:
            return self.price
    def get_html_price(self):
        if self.sale_price is not None:
            html_text= "<span class='sale-price'> %s </span><span <small  style='color:red;text-decoration:line-through;'> %s </span>"%(self.sale_price,self.price)
            return html_text
        else:
            html_text= "<span class='price'>%s</span>"% (self.price)

            return mark_safe(html_text)

    def get_absolute_url(self):
        return self.Product.get_absolute_url()
    def add_to_cart(self):
        return "%s?item=%s&qty=1"%(reverse("cartt"),self.id)
    def remov_from_cart(self):
        return "%s?item=%s&qty=1&delete=True" %(reverse("cartt"),self.id)
    def get_title(self):
        return "%s - %s" %(self.Product.title, self.title)
def product_post_saved_receiver(sender,instance,created,*args,**kwargs):
    Product = instance
    variations = Product.variotion_set.all()
    #if variations.count() == 0:
      #  new_var= Variotion()
       # new_var.Product= Product
       #new_var.title ='Default'
       # new_var.price = Product.price
       # new_var.save()
post_save.connect(product_post_saved_receiver,sender=Product)
def img_uplod_to(instance,filename):
    title = instance.Product.title
    sulg = slugify(title)
    return "product/%s/%s"%(sulg,filename)


class ProductImage(models.Model):
    Product= models.ForeignKey(Product)
    image = models.ImageField(upload_to=img_uplod_to)

    def __unicode__(self):
        return self.Product.title

class Category(models.Model):
    title = models.CharField(max_length=120,unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(null=True,blank=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True,auto_now=False)
    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("category_detail",kwargs={"slug": self.slug})

def img_uplod_to_featured(instance,filename):
    title = instance.product.title
    sulg = slugify(title)
    return "product/%s/featured/%s"%(sulg,filename)


class ProductFeatured(models.Model):
    product = models.ForeignKey(Product)
    image = models.ImageField(upload_to=img_uplod_to_featured)
    title = models.CharField(max_length=120,null=True,blank=True)
    text = models.CharField(max_length=220, null=True,blank=True)
    text_right = models.BooleanField(default=False)
    show_price = models.BooleanField(default=False)
    make_image_background = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.product.title

