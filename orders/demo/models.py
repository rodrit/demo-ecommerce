from django.db import models



class Order(models.Model):
    id = models.AutoField(primary_key=True)
    date_time = models.DateTimeField(null=False, blank=False)

    class Meta:
        managed = True
        verbose_name_plural = 'Orders'

    def __str__(self):
        return "Orden n° {} del {}".format(self.id, self.date_time)

    def get_total(self):
        total = 0
        for detail in self.details.all():
            total = total + detail.price
        return total



class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True, null=False, blank=False)
    price = models.FloatField(null=False,blank=False)

    class Meta:
        managed = True
        verbose_name_plural = 'Products'
    def __str__(self):
        return self.name


class OrderDetail(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='details')
    cuantity = models.IntegerField(null=False, blank=False)
    price = models.FloatField(blank=True , editable=False)
    product = models.ForeignKey('Product', on_delete=models.PROTECT, null=False, blank=False, related_name='orderdetails', validators=[])

    class Meta:
        managed = True
        verbose_name_plural = 'Order Details'
        unique_together = ['order', 'product']

    def __str__(self):
        return "order n° {} detail: {} {} ".format(self.order.id, self.cuantity, self.product )

    def save(self, *args, **kwargs):
        self.price = self.cuantity * self.product.price
        super().save(*args,**kwargs)
