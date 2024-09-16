from django.db import models
from users.models import CustomUser

class Match(models.Model):
    team_a = models.CharField(max_length=100)
    team_b = models.CharField(max_length=100)
    team_a_image = models.ImageField(upload_to='team_images/', null=True, blank=True)
    team_b_image = models.ImageField(upload_to='team_images/', null=True, blank=True)
    start_time = models.DateTimeField()
    final_score = models.CharField(max_length=20, null=True, blank=True)  # Store the result later

    def __str__(self):
        return f'{self.team_a} vs {self.team_b}'

class Odds(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='odds')
    outcome = models.CharField(max_length=10, choices=[('win', 'Win'), ('lose', 'Lose'), ('draw', 'Draw')])
    odds_value = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f'{self.match} - {self.outcome} ({self.odds_value})'



class Bet(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bets')
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='bets')
    odds = models.ForeignKey(Odds, on_delete=models.CASCADE)
    bet_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_winner = models.BooleanField(default=False)  # Set this after the match result is known
    payout = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f'Bet on {self.match} by {self.user}'


class BetSlip(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bet_slips')
    bets = models.ManyToManyField(Bet)  # A BetSlip can contain multiple individual Bets
    total_bet_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'BetSlip by {self.user} - Total: {self.total_bet_amount}'
