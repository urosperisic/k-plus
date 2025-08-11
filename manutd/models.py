from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver


class Player(models.Model):
    POSITION_CHOICES = [
        ('GK', 'Goalkeeper'),
        ('DF', 'Defender'),
        ('MF', 'Midfielder'),
        ('FW', 'Forward'),
    ]

    shirt_number = models.PositiveIntegerField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, unique=True)
    position = models.CharField(max_length=2, choices=POSITION_CHOICES)
    goals = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.shirt_number} - {self.first_name} {self.last_name}"


class Match(models.Model):
    HOME_AWAY_CHOICES = [
        ('H', 'Home'),
        ('A', 'Away'),
    ]

    PREMIER_LEAGUE_TEAMS = [
        ('Arsenal', 'Arsenal'),
        ('Aston Villa', 'Aston Villa'),
        ('Bournemouth', 'Bournemouth'),
        ('Brentford', 'Brentford'),
        ('Brighton', 'Brighton'),
        ('Chelsea', 'Chelsea'),
        ('Crystal Palace', 'Crystal Palace'),
        ('Everton', 'Everton'),
        ('Fulham', 'Fulham'),
        ('Liverpool', 'Liverpool'),
        ('Luton', 'Luton'),
        ('Man City', 'Man City'),
        ('Man Utd', 'Man Utd'),
        ('Newcastle', 'Newcastle'),
        ('Nottingham Forest', 'Nottingham Forest'),
        ('Sheffield United', 'Sheffield United'),
        ('Southampton', 'Southampton'),
        ('Tottenham', 'Tottenham'),
        ('West Ham', 'West Ham'),
        ('Wolves', 'Wolves'),
    ]

    opponent = models.CharField(max_length=100, choices=PREMIER_LEAGUE_TEAMS)
    is_home = models.CharField(max_length=1, choices=HOME_AWAY_CHOICES)
    result = models.CharField(max_length=10)
    match_date = models.DateField()

    def __str__(self):
        return f"{'Home' if self.is_home == 'H' else 'Away'} vs {self.opponent} - {self.result}"


class Goal(models.Model):
    match = models.ForeignKey(Match, related_name='goals', on_delete=models.CASCADE)
    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        to_field='last_name',
        db_column='player_last_name'
    )
    count = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.player.last_name} x{self.count} in {self.match}"


# --- SIGNALS ---

@receiver(post_save, sender=Goal)
def recalc_goals_on_post_save(sender, instance, **kwargs):
    """
    Nakon dodavanja ili izmene Goal-a,
    preračunaj ukupan broj golova za igrača.
    """
    player = instance.player
    total = Goal.objects.filter(player=player).aggregate(models.Sum('count'))['count__sum'] or 0
    player.goals = total
    player.save()


@receiver(post_delete, sender=Goal)
def recalc_goals_on_delete(sender, instance, **kwargs):
    """
    Nakon brisanja Goal-a,
    preračunaj ukupan broj golova za igrača.
    """
    player = instance.player
    total = Goal.objects.filter(player=player).aggregate(models.Sum('count'))['count__sum'] or 0
    player.goals = total
    player.save()
