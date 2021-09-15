from django import forms
from django.core.exceptions import ValidationError
from django.http import Http404


class MoneyForm(forms.Form):
    money = forms.IntegerField()  # TODO: кастомное сообщение об ошибки, не работает

    class Meta:
        fields = ['money', ]

    def clean_money(self):  # TODO: почему это не работает??? ssss вижу, а ошибку нет
        money = int(self.data.get('money'))
        print(money)
        if money <= 0:
            print('sssss')
            raise ValidationError('Только больше 0')
        return money


class BetForm(forms.Form):
    bet = forms.IntegerField(min_value=1)

    class Meta:
        fields = ['bet', ]

    def clean_bet(self, money):
        bet = int(self.data.get('bet'))
        print(money)
        print(bet)
        if bet > money or bet <= 0:
            # raise ValidationError('Ставка не должна быть больше чем у вас денег')  # TODO: убрать ошибку??
            raise Http404()
        return bet
