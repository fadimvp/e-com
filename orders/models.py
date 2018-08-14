from decimal import Decimal
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save,post_save
from django.core.urlresolvers import reverse

from carts.models import Cart
import braintree
if settings.DEBUG:
    gateway = braintree.BraintreeGateway(
        braintree.Configuration(
            environment=braintree.Environment.Sandbox,
            merchant_id='f9hdgrhq7hn93t4z',
            public_key='ycn3nsz4bkwmvdyt',
            private_key='882ca7cbf5a46a78c7a943ef12f7e2ce'
        )
    )
    # gateway = braintree.BraintreeGateway(
    #     braintree.Configuration(
    #         environment=braintree.Environment.Sandbox,
    #         merchant_id=settings.BRAINTREE_MERCHANT_ID,
    #         public_key=settings.BRAINTREE_PUBLIC,
    #         private_key=settings.BRAINTREE_PRIVATE
    #     )
    # )


# Create your models here.


class UserCheckout(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,null=True,blank=True)
    email =models.EmailField(unique=True)
    braintree_id = models.CharField(max_length=120,null=True,blank=True)
    def __unicode__(self):  # python3 def __str__(self):
        return self.email
    @property
    def get_braintree_id(self):
        instance =self
        if not instance.braintree_id:
            # update it
            result = gateway.customer.create({
                "email": instance.email,
            })
            if result.is_success:
                instance.braintree_id = result.customer.id
                instance.save()
        return instance.braintree_id
    def get_client_token(self):
        customer_id =self.get_braintree_id
        # print customer_id

        if customer_id:
            client_token = gateway.client_token.generate({
                "customer_id": customer_id
            })
            return client_token
        return None
def update_braintree_id(sender,instance,*args,**kwargs):
    if not instance.braintree_id:
        instance.get_braintree_id
       # pass
post_save.connect(update_braintree_id,sender=UserCheckout)
ADDRESS_TYPE =(
    ('billing','Billing '),
    ('shipping','Shipping '),
)
class UserAddress(models.Model):
    user = models.ForeignKey(UserCheckout)
    type = models.CharField(max_length=120,choices=ADDRESS_TYPE,)
    street = models.CharField(max_length=120)
    city = models.CharField(max_length=120)
    state =models.CharField(max_length=120)
    zipcode =  models.CharField(max_length=120)
    def __unicode__(self):
        return self.street
    def get_address(self):
        return "%s, %s, %s %s" %(self.street,self.city,self.state,self.zipcode)
ORDER_STATUS_CHOICE =(
    ('created','Created'),
    ('paid','Paid'),
    ('shipped','Shipped'),
    ('refunded','Refunded'),
)

class Order(models.Model):
    status = models.CharField(max_length=120,choices=ORDER_STATUS_CHOICE,default='created')
    cart = models.ForeignKey(Cart)
    user = models.ForeignKey(UserCheckout,null=True)
    billing_address = models.ForeignKey(UserAddress,related_name='billing_address',null=True)
    shipping_address = models.ForeignKey(UserAddress,related_name='shipping_address',null=True)
    shipping_total_price= models.DecimalField(max_digits=50,decimal_places=2,default=2.99)
    order_total = models.DecimalField(max_digits=49,decimal_places=2)
    order_id = models.CharField(max_length=20,null=True,blank=True)
    def __unicode__(self):
        return str(self.cart.id )
    def get_absolute_url(self):
        return reverse("order_detail",kwargs={"pk": self.pk})
    def mark_completed(self,order_id =None):
        self.status ="paid"
        if order_id and not self.order_id:
            self.order_id =order_id
        self.save()

def order_pre_save(sender,instance,*args,**kwargs):
    shipping_total_price = instance.shipping_total_price
    cart_total= instance.cart.total
    order_total= round(Decimal(shipping_total_price) + cart_total,2)
    instance.order_total = order_total
pre_save.connect(order_pre_save,sender=Order)
#class Order(models.Model):
   #cart
   #usercheckout --> required
   # shipping address
   #billing address
   # shipping total price
   # order total (cart total + shipping )
   # order_id --> custom id
