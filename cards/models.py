from django.db import models
from django.core.validators import MaxValueValidator

# Create your models here.

class Set(models.Model):
    name = models.CharField(max_length=250, null=False)
    code = models.CharField(max_length=12, null=False)

    def __str__(self):
        return self.name

class Card(models.Model):
    name = models.CharField(max_length=255, null=False)
    type = models.CharField(max_length=40, null=False)
    frame_type = models.CharField(max_length=40, null=False, default='monster')
    effect = models.TextField(null=False)
    attack = models.IntegerField(null=True)
    defense = models.IntegerField(null=True)
    level_rank = models.IntegerField(validators=[MaxValueValidator(12)], null=True)
    spell_trap_race = models.CharField(max_length=30, null=True)
    monster_race = models.CharField(max_length=30, null=True)
    attribute = models.CharField(max_length=10, null=True)
    archetype = models.CharField(max_length=50, null=True)
    image = models.ImageField(upload_to='card_images/', null=False, default='card_images/default.jpg')

    def __str__(self):
        return self.name

class CardSet(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='card_sets')
    set = models.ForeignKey(Set, on_delete=models.CASCADE, related_name='card_sets')
    rarity = models.CharField(max_length=100, null=False)

    class Meta:
        unique_together = ('card', 'set', 'rarity')