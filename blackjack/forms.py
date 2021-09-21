from django import forms
# from django.core.exceptions import ValidationError
from django.http import Http404


class MoneyForm(forms.Form):
    """форма для ввода денег"""
    money = forms.IntegerField(min_value=1)  # TODO: кастомное сообщение об ошибки, не работает

    class Meta:
        fields = ['money', ]

    # def clean_money(self):  # TODO: почему это не работает??? ssss вижу, а ошибку нет, а ниже - есть ошибка
    #     money = int(self.data.get('money'))
    #     print(money)
    #     if money <= 0:
    #         # raise ValidationError('Только больше 0')
    #         raise Http404()
    #     return money


def get_money(request):
    """во вью достать из формы деньги и присвоить их в переменную MONEY"""
    if request.method == 'POST':
        form = MoneyForm(request.POST)
        if form.is_valid():
            # MONEY = form.cleaned_data.get('money')  # здесь идёт запись в переменную MONEY
            # print('денег', MONEY)
            request.session['money'] = form.cleaned_data.get('money')
            # MONEY = request.session['money']
            # return MONEY


class BetForm(forms.Form):
    """форма для ввода ставки"""
    bet = forms.IntegerField(min_value=1)

    class Meta:
        fields = ['bet', ]

    def clean_bet(self, money):
        """проверка что ставка больше 0 и не больше чем всего денег"""
        bet = int(self.data.get('bet'))
        # print(money)
        # print(bet)
        if bet > money or bet <= 0:
            # raise ValidationError('Ставка не должна быть больше чем у вас денег')  # TODO: убрать ошибку??
            raise Http404()
        return bet


def get_bet(request):
    """для вью - достать ставку из формы, записать в переменную BET"""
    if request.method == 'POST':
        form = BetForm(request.POST)
        if form.clean_bet(request.session['money']):
            # BET = int(form.data.get('bet'))
            # print('ставка', BET)
            # print('денег', money)
            request.session['bet'] = int(form.data.get('bet'))
            # BET = request.session['bet']
            # return BET
