"""Models for the read_only_site app"""

from django.db import models
from trueskill import Rating, backends, rate_1vs1, setup

# More details about the constants on https://trueskill.org
# the initial mean of ratings
TRUESKILL_MU = 300.0
# the initial standard deviation of ratings. The recommended value is a third of mu.
TRUESKILL_SIGMA = 100.0
# the distance which guarantees about 76% chance of winning.
# The recommended value is a half of sigma.
TRUESKILL_BETA = 50.0
# the dynamic factor which restrains a fixation of rating.
# The recommended value is sigma per cent.
TRUESKILL_TAU = 3.0

class Player(models.Model):
    """Manages a player during a league"""
    discord_id = models.IntegerField(default=0, blank=True, null=True)
    discord_handle = models.CharField(max_length=200, default=None)
    discord_nickname = models.CharField(max_length=200, default=None)
    jstris_handle = models.CharField(max_length=200, default=None)
    signup_date = models.DateTimeField(auto_now_add=True)
    trueskill_mu = models.FloatField(default=TRUESKILL_MU)
    trueskill_sigma = models.FloatField(default=TRUESKILL_SIGMA)
    banned = models.BooleanField(default=False)
    def __str__(self):
        """Returns a string in the format discord_nickname/jstris_handle to display"""
        return self.discord_nickname + '/' + self.jstris_handle

class Match(models.Model):
    """Manages a league match, in a tournament or not"""
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
    tournament_match = models.BooleanField(default=False)
    def __str__(self):
        return (self.player_1.discord_nickname +
                ' VS ' +
                self.player_2.discord_nickname +
                ' on ' +
                str(self.played_on))
    def save(self):
        """Registers a match in the database"""
        if self.player_1.banned or self.player_2.banned:
            raise Exception('Can\'t play a match against a banned player!')
        if not self.pk:  # object is being created, thus no primary key field yet
            self.rate_match()
        return super(Match, self).save()
    def rate_match(self):
        """Use TrueSkill to modify players skill"""
        # TrueSkill setup
        setup(mu=TRUESKILL_MU, sigma=TRUESKILL_SIGMA, beta=TRUESKILL_BETA, tau=TRUESKILL_TAU)
        if 'scipy' in backends.available_backends():
            # scipy can be used in the current environment
            backends.choose_backend(backend='scipy')
        self.player_1_trueskill_mu_before_match = self.player_1.trueskill_mu
        self.player_1_trueskill_sigma_before_match = self.player_1.trueskill_sigma
        self.player_2_trueskill_mu_before_match = self.player_2.trueskill_mu
        self.player_2_trueskill_sigma_before_match = self.player_2.trueskill_sigma
        player_1_trueskill = Rating(self.player_1_trueskill_mu_before_match,
                                    self.player_1_trueskill_sigma_before_match)
        player_2_trueskill = Rating(self.player_2_trueskill_mu_before_match,
                                    self.player_2_trueskill_sigma_before_match)
        if self.winner == self.player_1:
            new_player_1_trueskill, new_player_2_trueskill = rate_1vs1(player_1_trueskill,
                                                                       player_2_trueskill)
        else:
            new_player_2_trueskill, new_player_1_trueskill = rate_1vs1(player_2_trueskill,
                                                                       player_1_trueskill)
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
