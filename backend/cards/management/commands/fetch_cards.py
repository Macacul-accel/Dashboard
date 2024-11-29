import requests
import logging
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from cards.models import Set, Card, CardSet

logger = logging.getLogger('fetch_cards')

class Command(BaseCommand):
    help = 'Insertion des cartes dans la base de donnée'

    def handle(self, *args, **kwargs):
        url = "https://db.ygoprodeck.com/api/v7/cardinfo.php"

        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            cards_data = response.json().get('data')
            
            for card_data in cards_data:
                try:
                    card_name = card_data.get('name')
                    card_type = card_data.get('type')
                    card_race = card_data.get('race')

                    if card_type in ['Spell Card', 'Trap Card']:
                        spell_trap_race = card_race
                        monster_race = None
                    else:
                        monster_race = card_race
                        spell_trap_race = None
                    card, _ = Card.objects.update_or_create(
                        name = card_name,
                        defaults={
                            'type': card_type,
                            'frame_type': card_data.get('frameType'),
                            'effect': card_data.get('desc'),
                            'attack': card_data.get('atk'),
                            'defense': card_data.get('def'),
                            'level_rank': card_data.get('level'),
                            'spell_trap_race': spell_trap_race,
                            'monster_race': monster_race,
                            'attribute': card_data.get('attribute'),
                            'archetype': card_data.get('archetype'),
                        },
                    )
                    existing_sets = {s.name: s for s in Set.objects.all()}

                    for set_data in card_data.get('card_sets', []):
                        set_name = set_data.get('set_name')
                        set_obj = existing_sets.get(set_name)

                        if not set_obj:
                            set_obj, _ = Set.objects.get_or_create(
                                name=set_name,
                                code=set_data.get('set_code'),
                            )
                            existing_sets[set_name] = set_obj

                        try:
                            CardSet.objects.get_or_create(
                                card=card,
                                set=set_obj,
                                rarity=set_data.get('set_rarity'),
                            )
                        except IntegrityError:
                            self.stderr.write(f"✅ Pour la carte {card_data.get('name')} la rareté {set_data.get('set_rarity')} a déjà été enregistrée dans le set {set_obj.get('set_name')}.")
                        except Exception as error:
                            self.stderr.write(f"❌ Erreur inattendue pour la carte '{card_data.get('name')}': {error}")

                    self.stdout.write(f"✅ Carte {card_data.get('name')} enregistrée !")

                except Exception as error:
                    logger.error(f"❌ Erreur dans la récupération de la carte {card_data.get('name')}: {error}", exc_info=True)

        except requests.exceptions.RequestException as error:
            self.stderr.write(f"❌ Erreur dans l'insertion: {error}")

        self.stdout.write("✅ Les cartes et les sets ont été enregistrés dans la base de donnée.")