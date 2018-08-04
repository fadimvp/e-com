from django.db import models

# Create your models here.
class  Signup (models.Model):

    email = models.EmailField()
    name = models.CharField(max_length=25)
    updata = models.DateTimeField(auto_now_add=False,auto_now=True)
    def __unicode__(self):
        return self.email
