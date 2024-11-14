from django.db import models
from django.core.validators import MaxValueValidator

# Create your models here.

class Set(models.Model):
    name = models.CharField(max_length=250, null=False)
    code = models.CharField(max_length=5, null=False)

    def __str__(self):
        return self.name

class Card(models.Model):
    name = models.CharField(max_length=255, null=False)
    type = models.CharField(max_length=40, null=False)
    effect = models.TextField(null=False)
    attack = models.CharField(max_length=7, null=True)
    defense = models.CharField(max_length=7, null=True)
    level_rank = models.IntegerField(validators=[MaxValueValidator(12)], null=True)
    race = models.CharField(max_length=30, null=True)
    attribute = models.CharField(max_length=10, null=True)
    archetype = models.CharField(max_length=20, null=True)
    image = models.ImageField(upload_to='card_images/', null=True)

    def __str__(self):
        return self.name

class CardSet(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='card_sets')
    set = models.ForeignKey(Set, on_delete=models.CASCADE, related_name='card_sets')
    rarity = models.CharField(max_length=15, null=False)

    class Meta:
        unique_together = ('card', 'set', 'rarity')