from django.shortcuts import render

from .logic import starting_draw


def base_view(request):
    template_name = 'blackjack/base.html'

    dealer_score, player_score, urls = starting_draw()

    context = {'url1': urls[0], 'url2': urls[1], 'url3': urls[2], 'url4': urls[3],
               'dealer_result': dealer_score,
               'player_result': player_score}
    return render(request, template_name, context)


def draw(request):
    ...
