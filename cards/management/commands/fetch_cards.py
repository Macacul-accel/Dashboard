import requests
from django.core.management.base import BaseCommand
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.db import IntegrityError
from cards.models import Set, Card, CardSet

class Command(BaseCommand):
    help = 'Insertion des cartes dans la base de donnée'

    def handle(self, *args, **kwargs):
        url = "https://db.ygoprodeck.com/api/v7/cardinfo.php"
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            cards_data = response.json()['data']
            
            for card_data in cards_data:
                card, created = Card.objects.update_or_create(
                    name=card_data.get('name'),
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

                if created and card_data.get('card_images'):
                    image_url = card_data['card_images'][0].get('image_url')
                    if image_url:
                        try:
                            img_temp = NamedTemporaryFile(delete=True)
                            img_temp.write(requests.get(image_url).content)
                            img_temp.flush()
                            image_name = f"{card_data['name'].replace(' ', '_')}.jpg"
                            card.image.save(image_name, File(img_temp))
                            self.stdout.write(f"L'image pour {card.name} a été téléchargée avec succès")
                        except requests.exceptions.RequestException as exception:
                            self.stderr.write(f"L'image pour {card.name} n'a pas pu être téléchargée: {exception}")
                    else:
                        self.stdout.write(f"L'image pour {card.name} est indisponible, url non existant")

                for set_data in card_data.get('card_sets',[]):
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
                        self.stderr.write(f"Pour la carte {card.name}, la rareté {set_data.get('set_rarity')} a déjà été enregistrée dans le set {set_obj.name}.")

                self.stdout.write(f"Carte {card.name} enregistrée !")

        except requests.exceptions.RequestException as exception:
            self.stderr.write(f"Erreur dans l'insertion: {exception}")
        
        self.stdout.write("Les cartes et les sets ont été enregistrés dans la base de donnée.")