from django import template


register = template.Library()


@register.inclusion_tag('blackjack/show_money_and_bet.html')
def show_money_and_bet(money=None, bet=None):
    context = {
        'money': money,
        'bet': bet
    }
    return context
