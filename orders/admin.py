from django.contrib import admin
from .models import *

class ProductInOrderInline(admin.TabularInline):
    model = ProductInOrder
#   количество рядов по умолчанию
    extra = 0

# берет модель из МЕТА и перенастраивает ее как нам удобно
class StatusAdmin (admin.ModelAdmin):
    # list_display = ["name", "email"]

    #  Итератор который достает имя для каждого поля в таблице(когда много полей)
    list_display = [field.name for field in Status._meta.fields]
    # Убирает отображение выбранного поля
    # exclude = ["email"]
    # Опция филтрации по введенным значениям полей
    # search_fields = ["name", "email"]
    # справа отображается фильтр по ыбранным полям
    # list_filter = ('name',)
    # Отображается  ТОЛЬКО выбрааные поля
    # fields = ["email"]
    # exclude = ["email"]
    # search_fields = ['category', 'subCategory', 'suggestKeyword']
    # inlines = [FieldMappingInline]
    class Meta:
        model = Status


# регистрируем модели для отображения в админке
admin.site.register(Status, StatusAdmin)

#  CTR + R - Заменить фразу во всем участке кода
class OrderAdmin (admin.ModelAdmin):
    list_display = [field.name for field in Order._meta.fields]
    inlines = [ProductInOrderInline]
    class Meta:
        model = Order

admin.site.register(Order, OrderAdmin)


class ProductInOrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductInOrder._meta.fields]

    class Meta:
        model = ProductInOrder


admin.site.register(ProductInOrder, ProductInOrderAdmin)



class ProductInBasketAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductInBasket._meta.fields]

    class Meta:
        model = ProductInBasket


admin.site.register(ProductInBasket, ProductInBasketAdmin)


