from django_filters import FilterSet, CharFilter, ChoiceFilter, RangeFilter
from django import forms
from .models import Card, Set
from .constant import *


class CardFilterSet(FilterSet):
    """
    Filtre pour le model Card, permettant d'obtenir les cartes souhaitées selon certains critères.
    Les variables *CHOICES sont dans le fichier 'constant.py'.
    """
    name = CharFilter(field_name='name', lookup_expr='icontains', label='Nom de carte', widget=forms.TextInput(attrs={'placeholder': 'Rechercher par nom'}))
    type = ChoiceFilter(choices=MONSTER_TYPE_CHOICES, method='filter_by_monster_type', label='Autre', empty_label='Tous')
    frame_type = ChoiceFilter(choices=FRAME_TYPE_CHOICES, method='filter_by_frametype', label='Type de carte', empty_label='Tous')
    attack = RangeFilter(label='Attaque', widget=forms.NumberInput(attrs={'class': 'custom-range', 'placeholder': 'Min-Max'}))
    defense = RangeFilter(label='Défense', widget=forms.NumberInput(attrs={'class': 'custom-range', 'placeholder': 'Min-Max'}))
    level_rank = RangeFilter(label="Niveau/Rang", widget=forms.NumberInput(attrs={'class': 'custom-range', 'placeholder': 'Min-Max'}))
    spell_trap_race = ChoiceFilter(choices=SPELL_TRAP_RACE_CHOICES, method='filter_by_spell_trap_race', label='Type de magie, piège', empty_label='Tous')
    monster_race = ChoiceFilter(choices=MONSTER_RACE_CHOICES, method='filter_by_monster_race', label='Type de monstre', empty_label='Tous')
    attribute = ChoiceFilter(choices=MONSTER_ATTRIBUTE_CHOICES, method='filter_by_monster_attribute', label='Attribut', empty_label='Tous')
    set_code = ChoiceFilter(
        field_name='card_sets__set__code', 
        label='Code du set', 
        empty_label='Tous',
        choices=lambda: [(set_.code, set_.name) for set_ in Set.objects.all()],
        method='filter_by_set_code'
    )

    class Meta:
        model = Card
        fields = ['name', 'type','frame_type', 'attack', 'defense', 'level_rank', 'spell_trap_race', 'monster_race', 'attribute', 'set_code']


    def filter_by_frametype(self, queryset, name, value):
        """
        Fonctions pour récupérer les mots clés de chaque filtre et laisser le choix aux utilisateurs avec des filtres prédéfinis.
        """
        return filter_by_mapping(queryset, FRAME_TYPE_MAPPING, name, value, 'frame_type')

    def filter_by_monster_type(self, queryset, name, value):
        return filter_by_mapping(queryset, MONSTER_TYPE_MAPPING, name, value, 'type')

    def filter_by_spell_trap_race(self, queryset, name, value):
        return filter_by_mapping(queryset, SPELL_TRAP_RACE_MAPPING, name, value, 'spell_trap_race')

    def filter_by_monster_race(self, queryset, name, value):
        return filter_by_mapping(queryset, MONSTER_RACE_MAPPING, name, value, 'monster_race')

    def filter_by_monster_attribute(self, queryset, name, value):
        return filter_by_mapping(queryset, MONSTER_ATTRIBUTE_MAPPING, name, value, 'attribute')

    def filter_by_set_code(self, queryset, name, value):
        """
        Filtre en fonction du code du set.
        """
        return queryset.filter(card_sets__set__code=value).distinct()