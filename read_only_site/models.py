from django.db import models
from pprint import pformat
from trueskill import Rating, rate_1vs1, backends, setup

# Create your models here.
class Player(models.Model):
    discord_handle = models.CharField(max_length=200, default=None)
    signup_date = models.DateTimeField(auto_now_add=True)
    trueskill_mu = models.FloatField(default=25.0)
    trueskill_sigma = models.FloatField(default=8.333)
    def __str__(self):
        return self.discord_handle + ' ' + str(self.trueskill_mu) + ' ' + str(self.trueskill_sigma)

class Match(models.Model):
    player_1 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='+')
    player_2 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='+')
    winner = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='+')
    match_identifier = models.CharField(max_length=200, blank=True, default='')
    played_on = models.DateTimeField(auto_now_add=True)
    player_1_trueskill_mu_before_match = models.FloatField(blank=True, default=0.0)
    player_1_trueskill_sigma_before_match = models.FloatField(blank=True, default=0.0)
    player_1_trueskill_mu_after_match = models.FloatField(blank=True, default=0.0)
    player_1_trueskill_sigma_after_match = models.FloatField(blank=True, default=0.0)
    player_2_trueskill_mu_before_match = models.FloatField(blank=True, default=0.0)
    player_2_trueskill_sigma_before_match = models.FloatField(blank=True, default=0.0)
    player_2_trueskill_mu_after_match = models.FloatField(blank=True, default=0.0)
    player_2_trueskill_sigma_after_match = models.FloatField(blank=True, default=0.0)
    tournament_match=models.BooleanField(default=False)
    def __str__(self):
        # TODO: better printer
        return self.player_1_name() + ' VS ' + self.player_2_name() + ' on ' + str(self.played_on)
    def player_1_name(self):
        return self.player_1.discord_handle
    def player_2_name(self):
        return self.player_2.discord_handle
    def save(self, *args, **kwargs):
        if not self.pk:  # object is being created, thus no primary key field yet
            self.rate_match()
        super(Match, self).save(*args, **kwargs)
    def rate_match(self):
        # TrueSkill setup
        setup(mu=300.0, sigma=200.0, beta=50.0, tau=3.0)
        if 'scipy' in backends.available_backends():
            # scipy can be used in the current environment
            backends.choose_backend(backend='scipy')
        self.player_1_trueskill_mu_before_match = self.player_1.trueskill_mu
        self.player_1_trueskill_sigma_before_match = self.player_1.trueskill_sigma
        self.player_2_trueskill_mu_before_match = self.player_2.trueskill_mu
        self.player_2_trueskill_sigma_before_match = self.player_2.trueskill_sigma
        player_1_trueskill = Rating(self.player_1_trueskill_mu_before_match, self.player_1_trueskill_sigma_before_match)
        player_2_trueskill = Rating(self.player_2_trueskill_mu_before_match, self.player_2_trueskill_sigma_before_match)
        if self.winner == self.player_1:
            new_player_1_trueskill, new_player_2_trueskill = rate_1vs1(player_1_trueskill, player_2_trueskill)
        else:
            new_player_2_trueskill, new_player_1_trueskill = rate_1vs1(player_2_trueskill, player_1_trueskill)
        self.player_1_trueskill_mu_after_match = new_player_1_trueskill.mu
        self.player_1_trueskill_sigma_after_match = new_player_1_trueskill.sigma
        self.player_2_trueskill_mu_after_match = new_player_2_trueskill.mu
        self.player_2_trueskill_sigma_after_match = new_player_2_trueskill.sigma
        self.player_1.trueskill_mu = self.player_1_trueskill_mu_after_match
        self.player_1.trueskill_sigma = self.player_1_trueskill_sigma_after_match
        self.player_2.trueskill_mu = self.player_2_trueskill_mu_after_match
        self.player_2.trueskill_sigma = self.player_2_trueskill_sigma_after_match
        self.player_1.save()
        self.player_2.save()
