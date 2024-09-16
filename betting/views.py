from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Match, Odds, Bet, BetSlip
from users.models import CustomUser
from django.db import transaction

# View to display upcoming matches
def match_list(request):
    matches = Match.objects.all()
    return render(request, 'betting/match_list.html', {'matches': matches})

# View to display odds and allow placing a bet
@login_required
def match_detail(request, match_id):
    match = get_object_or_404(Match, pk=match_id)
    odds = match.odds.all()  # Get all odds related to the match

    if request.method == 'POST':
        odds_id = request.POST.get('odds')
        bet_amount = request.POST.get('bet_amount')

        odds_instance = get_object_or_404(Odds, pk=odds_id)

        # Ensure the user has enough balance
        user = request.user
        if user.balance >= float(bet_amount):
            with transaction.atomic():  # Ensuring atomic transaction
                # Deduct the bet amount from the user's balance
                user.balance -= float(bet_amount)
                user.save()

                # Create the Bet
                bet = Bet.objects.create(
                    user=user,
                    match=match,
                    odds=odds_instance,
                    bet_amount=bet_amount
                )

                # Add the bet to a BetSlip (create BetSlip if it doesn't exist)
                bet_slip, created = BetSlip.objects.get_or_create(user=user)
                bet_slip.bets.add(bet)
                bet_slip.total_bet_amount += float(bet_amount)
                bet_slip.save()

            return redirect('betting:bet_slip')

    return render(request, 'betting/match_detail.html', {'match': match, 'odds': odds})

# View to display the user's current bet slip
@login_required
def bet_slip(request):
    user = request.user
    bet_slip = BetSlip.objects.filter(user=user).first()
    return render(request, 'betting/bet_slip.html', {'bet_slip': bet_slip})

# View to display the user's betting history
@login_required
def bet_history(request):
    user = request.user
    bets = Bet.objects.filter(user=user)
    return render(request, 'betting/bet_history.html', {'bets': bets})
