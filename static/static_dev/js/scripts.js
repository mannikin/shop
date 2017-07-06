/**
 * Created by User on 05.06.2017.
 */

//Id на странице Jquery считывает только одно, поэтому возьмет первое
// # - для id, . - для класса
$(document).ready(function() {
    //$- обращаямся к Jquery , # - выбираем элемент по id
    var form = $('#form_buying_product');
    console.log(form);

    function basketUpdating(product_id, nmb, is_delete){
        //Ajax - сохраняем данные о товаре в базе данных без перезагрузки страницы
        var data = {};
        data.product_id = product_id;
        data.nmb = nmb;
        // csrf_token специальный токен для создания POST запрос на сервер, зашиврован в виде "hidden" for safety
        var csrf_token = $('#form_buying_product [name="csrfmiddlewaretoken"]').val();
        data["csrfmiddlewaretoken"] = csrf_token;

        if (is_delete){
            data["is_delete"] = true;
        }

        //Считывает урл с атрибута  action в форме
        var url = form.attr("action");

        console.log(data);
        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            cache: true,
            success: function (data) {
                console.log("OK");
                console.log(data.products_total_nmb);
                //Добавляем текст(цифру) рядом с "Корзина"
                if (data.products_total_nmb || data.products_total_nmb == 0 ){
                    $('#basket_total_nmb').text("("+data.products_total_nmb+")");

                    console.log(data.products);
                    //очищаем ul строки, хз что это значит
                    $('.basket-items ul').html("");

                    //проходимся циклом по каждому объекту
                    //K - key, V - value
                    $.each(data.products, function(k, v){
                        // Отправляем форму в basket-item
                        $('.basket-items ul').append('<li>'+v.name+', ' + v.nmb + 'шт. ' + 'по ' +v.price_per_item+ ' UAH ' +
                        '<a class="delete-item" href="" data-product_id="'+v.id+'"> X</a>' +
                        '</li>');
                    });
                }
            },
            error: function() {
                console.log("error")
            }
        });
    }

    //переопределяем событие on.submit
    form.on('submit', function (e) {
        //предотвращаем поведение функции по-умолчании - перезагрузку страницы
        e.preventDefault();
        console.log('123');
        //послее того как перехватили отправку формы можем все пепеопределить
        //val - получить значение вызванного элемента
        // перехватываеи кол-во из inputa
        var nmb = $('#number').val();
        console.log(nmb);
        var submit_btn = $('#submit_btn');
        //считываем с кнопки аттрибуты
        var product_id = submit_btn.data("product_id");
        var product_name = submit_btn.data("name");
        var product_price = submit_btn.data("price");
        console.log(product_id);
        console.log(product_name);
        console.log(product_price);

        basketUpdating(product_id, nmb, is_delete=false)

    });

    // toggleClass - добавляет класс если нет, удаляет если есть
    function showingBasket(){
       $('.basket-items').removeClass('hidden');
    }
    //on - перечисляем события(клик или наведение) на кнопку "корзина"
    // $('.basket-container').on('click', function (e) {
    //     e.preventDefault();
    //     //убираем  класс hidden чтобы панель появилась
    //     shovingBasket()
    // });
    $('.basket-container').mouseover(function () {
        showingBasket();
    });

    // $('.basket-container').mouseout('click', function () {
    //      shovingBasket()
    // });

    //добавляем новый элемент удаления  delete-item
    // closest() - ближайший элемент li
    $(document).on('click', '.delete-item', function(e){
         e.preventDefault();
         // $(this).closest('li').remove();

        product_id = $(this).data("product_id");
        nmb = 0;
        basketUpdating(product_id, nmb, is_delete=true);
        console.log();
    });

    function calculatingBasketAmount() {
        var total_order_amount = 0;
        //проходимся по всем элементам с таким именем классса
        //parseInt - преобразует текст в число
        $('.total-product-in-basket-amount').each(function(){
            total_order_amount += parseFloat($(this).text()); 
        });
        //Вписываем результат в нужный span
        $('#total_order_amount').text(total_order_amount.toFixed(2))
    }

    //отслеживаем изменение кол-ва отдельного товара в чекауте
    $(document).on('change', ".product-in-basket-nmb", function(){
        var current_nmb = $(this).val();
        console.log(current_nmb);
        //находим значение ближайшего тега <TR> где мы меняем кол-во
        //обычно следующий
        var current_tr = $(this).closest('tr');
                //иЩем нужный span с таким классом ↓, и берем из него текст и INTуем
        var current_price = parseFloat(current_tr.find('.product-price').text()).toFixed(2);
        var total_amount = parseFloat(current_nmb * current_price).toFixed(2);

    //  После пересчета находим нужный ряд с нужным классом и обновляем значение
        current_tr.find('.total-product-in-basket-amount').text(total_amount);
        calculatingBasketAmount();
    });

    calculatingBasketAmount()


});