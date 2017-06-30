from django.contrib import admin
from .models import *


# берет модель из МЕТА и перенастраивает ее как нам удобно
class SubscriberAdmin (admin.ModelAdmin):
    # list_display = ["name", "email"]

    #  Итератор который достает имя для каждого поля в таблице(когда много полей)
    list_display = [field.name for  field in  Subscriber._meta.fields]
    # Убирает отображение выбранного поля
    # exclude = ["email"]
    # Опция филтрации по введенным значениям полей
    search_fields = ["name", "email"]

    # справа отображается фильтр по ыбранным полям
    list_filter = ('name',)


    # Отображается  ТОЛЬКО выбрааные поля
    fields = ["email"]

    # exclude = ["email"]
    # search_fields = ['category', 'subCategory', 'suggestKeyword']
    # inlines = [FieldMappingInline]
    class Meta:
        model = Subscriber


# регистрируем модели для отображения в админке
admin.site.register(Subscriber, SubscriberAdmin)
