from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(max_length=64,blank=True, null=True, default=None)
    is_active = models.BooleanField(default=True)

    def __str__ (self):
        return "%s" % self.name
                 # %s %s" % () множественное представление

    class Meta:
        # произносимое имя ед число
        verbose_name = 'Категория товара'
        # произносимое имя во множественном числе
        verbose_name_plural = 'Категория товара'

class Product(models.Model):
    name = models.CharField(max_length=64,blank=True, null=True, default=None)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount = models.IntegerField(default=0)
    category = models.ForeignKey(ProductCategory,blank=True, null=True, default=None)
    short_description = models.TextField(blank=True, null=True, default=None)
    description = models.TextField(blank=True, null=True, default=None)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)


    def __str__ (self):
        return "%s" % self.name
                 # %s %s" % () множественное представление

    class Meta:
        # произносимое имя ед число
        verbose_name = 'Товар'
        # произносимое имя во множественном числе
        verbose_name_plural = 'Товары'


class ProductImage(models.Model):
    # ЗДесь ссылка на продукт
    product = models.ForeignKey(Product,blank=True, null=True, default=None)
    #  upload_to= относительно папки MEDIA
    image = models.ImageField(upload_to='products_images/')
    is_main = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)


    def __str__ (self):
        return "%s" % self.id
                 # %s %s" % () множественное представление

    class Meta:
        # произносимое имя ед число
        verbose_name = 'Фотография'
        # произносимое имя во множественном числе
        verbose_name_plural = 'Фотографии'

