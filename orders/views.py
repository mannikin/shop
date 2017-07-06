from django.http import JsonResponse
from  .models import *
from django.shortcuts import render
# импортируем форму
from .forms import CheckoutContactForm
from django.contrib.auth.models import User

# въюха для  добавления в корзину
def basket_adding(request):
    return_dict = dict()
    # здесь ключ сессии уже создан
    session_key = request.session.session_key
    print (request.POST)

    # достаем Product_id и nmb из request.POST
    data = request.POST
    product_id = data.get("product_id")
    nmb = data.get("nmb")
    is_delete = data.get("is_delete")

    if is_delete == 'true':

        ProductInBasket.objects.filter(id=product_id).update(is_active=False)


    else:

        # update_or_create - фунцкция создает либо обнавляет существующую запись
        new_product, created = ProductInBasket.objects.get_or_create(session_key=session_key, product_id=product_id, is_active=True, defaults={"nmb": nmb})
        if not created:
            print("not created")
            new_product.nmb += int(nmb)
            new_product.save(force_update=True)


    # Здесь процесс сохранения информациии о заказанных товарах
    # в корзинена стороне браузера

    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True)
    products_total_nmb = products_in_basket.count()
    return_dict["products_total_nmb"] = products_total_nmb

    return_dict["products"] = list()

    for item in products_in_basket:
        product_dict = dict()
        product_dict["id"] = item.id
        product_dict["name"] = item.product.name
        product_dict["price_per_item"] = item.price_per_item
        product_dict["nmb"] = item.nmb
        #после того как создали словарьего необходимо добавить
        # к финальнму листу с помощью .append
        return_dict["products"].append(product_dict)

    return JsonResponse(return_dict)


# 2.Создаем во вьюхе checkout функцию

def checkout(request):
    # Достаем все записи из модели ProductInBasket,
    # чтобы передать их в шаблон для работы
    session_key = request.session.session_key
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True)
    for item in products_in_basket:
        print(item.order)
    # форма принимает  значеение request.POST или ничего.
    # после отрисовки форммы здесь она будет работать в шаблоне
    form = CheckoutContactForm(request.POST or None)

    #Смотрим что присылает нам форма
    # не забудь указать на форме метод(post) и токен и имя на INPUT
    # иначе приходить ничего не будет
    if request.POST:
        print(request.POST)
        # Проверяем все ли правильно  в  присланной форме
        if form.is_valid():
            print("Valid=Yes")
            data = request.POST
            # .get - предотврвтит ошибку если поле пустое.[..., xxx] - присвоить значение ххх если поле пустое
            name = data.get("name", "23456")
            phone = data["phone"]
            # берем или создаем юзера если еще не создан
            user, created = User.objects.get_or_create(username=phone, defaults={"first_name": name})


            # делаем сам заказ

            order = Order.objects.create(user=user, customer_name=name, customer_phone=phone, status_id=6)

        #     считываем информацию о заказе
        #     проходимся по словарю таким образом
            for name, value in data.items():
                if name.startswith("product_in_basket_"):
                    product_in_basket_id = name.split("product_in_basket_")[1]
                    # считываем элемент по id
                    product_in_basket = ProductInBasket.objects.get(id=product_in_basket_id)
                    print(type(value))
                    product_in_basket.nmb = value
                    product_in_basket.order = order
                    product_in_basket.save(force_update=True)


                    ProductInOrder.objects.create(product=product_in_basket.product,
                                                  nmb=product_in_basket.nmb,
                                                  price_per_item=product_in_basket.price_per_item,
                                                  total_price=product_in_basket.total_price,
                                                  order=order,)


    else:
        print("No")
    return render(request, 'orders/checkout.html', locals())
#  После этого создаем шаблон п оадресу orders/checkout
