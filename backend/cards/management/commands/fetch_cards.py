import requests
import logging
from django.core.management.base import BaseCommand
from cards.models import Card

logger = logging.getLogger('fetch_cards')

class Command(BaseCommand):
    help = 'Insertion des cartes dans la base de donnée'

    def handle(self, *args, **kwargs):
        url = "https://db.ygoprodeck.com/api/v7/cardinfo.php"

        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            cards_data = response.json().get('data')
            
            
            if not cards_data:
                self.stderr.write("❌ Aucune donnée trouvée dans la réponse API.")
                return

            for card_data in cards_data:
                try:
                    card_name = card_data.get('name')
                    card_type = card_data.get('type')
                    card_race = card_data.get('race')

                    logger.info(f"Processing card: {card_name}")

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

                    self.stdout.write(f"✅ Carte {card_data.get('name')} enregistrée !")

                except Exception as error:
                    logger.error(f"❌ Erreur dans la récupération de la carte {card_data.get('name')}: {error}", exc_info=True)

        except requests.exceptions.RequestException as error:
            self.stderr.write(f"❌ Erreur dans l'insertion: {error}")

        self.stdout.write("✅ Les cartes et les sets ont été enregistrés dans la base de donnée.")