from django.db import models



class Blogpost(models.Model):
    post_id =  models.AutoField(primary_key=True)
    title = models.CharField(max_length=300,default="")
    pub_date = models.DateField( )
    head0 =models.CharField(max_length=500,default=0)
    chead0 = models.CharField(max_length=5000, default=0)
    head1 = models.CharField(max_length=500,default=0)
    chead1 = models.CharField(max_length=5000, default=0)
    head2 =models.CharField(max_length=500,default=0)
    chead2 = models.CharField(max_length=5000, default=0)
    thumbnail = models.ImageField(upload_to="shop/images",default="")
    def __str__(self):
        return self .title