import requests
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from cards.models import Set, Card, CardSet

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
                    card, _ = Card.objects.update_or_create(
                        name = card_name,
                        defaults={
                            'type': card_data.get('type'),
                            'effect': card_data.get('desc'),
                            'attack': card_data.get('atk'),
                            'defense': card_data.get('def'),
                            'level_rank': card_data.get('level'),
                            'race': card_data.get('race'),
                            'attribute': card_data.get('attribute'),
                        },
                    )

                    print(f"Card object created or updated: {card}, card type: {type(card)}")

                    if card_data['card_sets']:
                        for set_data in card_data['card_sets']:
                            set_obj, _ = Set.objects.get_or_create(
                                name=set_data.get('set_name'),
                                code= set_data.get('set_code')
                            )

                            try:
                                CardSet.objects.get_or_create(
                                    card=card,
                                    set=set_obj,
                                    rarity=set_data.get('set_rarity')
                                )
                            except IntegrityError:
                                self.stderr.write(f"Pour la carte {card_data.get('name')} la rareté {set_data.get('set_rarity')} a déjà été enregistrée dans le set {set_obj.get('set_name')}.")
                    else:
                        self.stderr.write(f"Pas de set pour {card_data.get('name')}")

                    self.stdout.write(f"Carte {card_data.get('name')} enregistrée !")

                except Exception as error:
                    self.stderr.write(f"Erreur dans la récupération de la carte {card_data.get('name')}: {error}")

        except requests.exceptions.RequestException as error:
            self.stderr.write(f"Erreur dans l'insertion: {error}")

        self.stdout.write("Les cartes et les sets ont été enregistrés dans la base de donnée.")