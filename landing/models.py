from django.db import models

class Subscriber(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=120)

    def __str__ (self):  # Презентует в админке то как будет выглядеть объект
        return " Пользователь: %s Почта: %s" % (self.name, self.email)   # Subdscriber, тоесть его логическое имя
                                                   # %s %s" % () множественное представление

    class Meta:
        verbose_name = 'Каждый подписчик здесь'  # произносимое имя
        verbose_name_plural = 'Подписчики'  # произносимое имя во множественном числе