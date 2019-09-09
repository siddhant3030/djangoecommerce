from django.db import models

class OrderItem(models.Model):
    pass

class Order(models.Model):
    pass

class Item(models.Model):
    title = models.CharField(max_length = 100)

    def _str_(self):
        return self.title
