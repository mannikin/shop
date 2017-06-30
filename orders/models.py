from django.db import models
from products.models import Product
# библиатека для переопределения сохранений в моделях
from django.db.models.signals import post_save
# библ. для создания авторизации пользователя
from django.contrib.auth.models import User


class Status(models.Model):
    name = models.CharField(max_length=24, blank=True, null=True, default=None)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    # Презентует в админке то как будет выглядеть объект
    # Status тоесть его логическое имя
    def __str__ (self):
        return " %s" % self.name
                 # %s %s" % () множественное представление
    class Meta:
        # произносимое имя ед число
        verbose_name = 'Статус заказа'
        # произносимое имя во множественном числе
        verbose_name_plural = 'Статусы заказа'






class Order(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, default=None)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    # total price for all products in order
    customer_name = models.CharField(max_length=64,blank=True, null=True, default=None)
    customer_email = models.EmailField(blank=True, null=True, default=None)
    # Blank=true - может быть пустое поле
    customer_phone = models.CharField(max_length=48,blank=True, null=True, default=None)
    customer_address = models.CharField(max_length=128,blank=True, null=True, default=None)
    comments = models.TextField(blank=True, null=True, default=None)
    status = models.ForeignKey(Status)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    # Презентует в админке то как будет выглядеть объект
    # Order, тоесть его логическое имя
    def __str__(self):
        return " %s %s" % (self.id, self.status.name)
                 # %s %s" % () множественное представление

    class Meta:
        # произносимое имя ед число
        verbose_name = 'Заказ'
        # произносимое имя во множественном числе
        verbose_name_plural = 'Заказы'

    def save(self, *args, **kwargs):

       super(Order, self).save(*args, **kwargs)

class ProductInOrder(models.Model):
    # Делаем ссылку на заказ - привязка JOIN
    order = models.ForeignKey(Order, blank=True, null=True, default=None)
    product = models.ForeignKey(Product, blank=True, null=True, default=None)
    nmb = models.IntegerField(default=1)
    price_per_item = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_price =models.DecimalField(max_digits=12, decimal_places=2, default=0)  # price * nmb
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    # Презентует в админке то как будет выглядеть объект
    # ProductInOrder, тоесть его логическое имя
    def __str__(self):
        return " %s" % self.product.name
                 # %s %s" % () множественное представление

    class Meta:
        # произносимое имя ед число
        verbose_name = 'Товар в заказе'
        # произносимое имя во множественном числе
        verbose_name_plural = 'Товары в заказе'

    # шаблон для переопределения метода чтобы прописать логику вручную
    def save(self, *args, **kwargs):
        price_per_item = self.product.price
        self.price_per_item = price_per_item

        self.total_price = int(self.nmb) * self.price_per_item

        super(ProductInOrder, self).save(*args, **kwargs)

# Специальная функция которая отрабатывает после метода save выше
def product_in_order_post_save(sender, instance, created, **kwargs):
    # создаем список активных заказов
    order = instance.order
    all_products_in_order = ProductInOrder.objects.filter(order=order, is_active=True)

    order_total_price = 0
    for item in all_products_in_order:
        order_total_price += item.total_price

    instance.order.total_price = order_total_price
    # сохраняем запись с параметром точно ОБНОВИТЬ, а не делать новую запись
    instance.order.save(force_update=True)

post_save.connect(product_in_order_post_save, sender=ProductInOrder)



class ProductInBasket(models.Model):
    session_key = models.CharField(max_length=128, blank=True, null=True, default=None)
    order = models.ForeignKey(Order, blank=True, null=True, default=None)
    product = models.ForeignKey(Product, blank=True, null=True, default=None)
    nmb = models.IntegerField(default=1)
    price_per_item = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_price =models.DecimalField(max_digits=12, decimal_places=2, default=0)  # price * nmb
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    # Презентует в админке то как будет выглядеть объект
    # ProductInBasket, тоесть его логическое имя
    def __str__(self):
        return "%s" % self.product.name
        # %s %s" % () множественное представление

    class Meta:
        # произносимое имя ед число
        verbose_name = 'Товар в Корзине'
        # произносимое имя во множественном числе
        verbose_name_plural = 'Товары в корзине'

    # шаблон для переопределения метода чтобы прописать логику вручную
    # цена за штуку, и цена шт * цену = тотал
    def save(self, *args, **kwargs):
        price_per_item = self.product.price
        self.price_per_item = price_per_item
        self.total_price = int(self.nmb) * price_per_item

        super(ProductInBasket, self).save(*args, **kwargs)