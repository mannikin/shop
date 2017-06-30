from django.shortcuts import render
from .forms import SubscriberForm
from products.models import *

def landing(request):

    form = SubscriberForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        print(request.POST)
        print(form.cleaned_data)
        data = form.cleaned_data

        print(form.cleaned_data["name"])
        print(data["name"])

        new_form = form.save()

    return render(request, 'landing/landing.html', locals())


# Выводим все ТОВАРЫ на страницу home.html
def home(request):
    # Выводим только активные товары
    products_images = ProductImage.objects.filter(is_active=True, is_main=True, product__is_active=True,)
    # Как бы быстрый способ сослаться на значение в аргументах
    products_images_phones = products_images.filter(product__category__id=1)
    products_images_laptops = products_images.filter(product__category__id=2)
    # Фннккция locals() берет все переменные и прокидывает в шаблон
    return render(request, 'landing/home.html', locals())