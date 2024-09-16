from django.contrib import admin
from .models import Match, Odds, Bet, BetSlip

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('team_a', 'team_b', 'start_time', 'final_score')
    search_fields = ('team_a', 'team_b')
    list_filter = ('start_time',)

@admin.register(Odds)
class OddsAdmin(admin.ModelAdmin):
    list_display = ('match', 'outcome', 'odds_value')
    list_filter = ('outcome',)

@admin.register(Bet)
class BetAdmin(admin.ModelAdmin):
    list_display = ('user', 'match', 'odds', 'bet_amount', 'is_winner', 'payout')
    search_fields = ('user__username', 'match__team_a', 'match__team_b')
    list_filter = ('is_winner',)

@admin.register(BetSlip)
class BetSlipAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_bet_amount')
    search_fields = ('user__username',)
