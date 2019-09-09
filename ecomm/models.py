from django.db import models

class OrderItem(models.Model):
    title = models.CharField(max_length = 100)
    def _str_(self):
        return self.title


class Order(models.Model):
    title = models.CharField(max_length = 100)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    
    def _str_(self):
        return self.title


class Item(models.Model):
    title = models.CharField(max_length = 100)


    def _str_(self):
        return self.title
