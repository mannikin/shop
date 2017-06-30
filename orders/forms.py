from django import forms
from .models import *

class CheckoutContactForm(forms.Form):

    # Пишем поля с которыми форма будет работать
    name = forms.CharField(required=True)
    phone = forms.CharField(required=True)

# После создания формы импортируем на вьюху
