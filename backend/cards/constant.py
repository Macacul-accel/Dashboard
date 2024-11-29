def filter_by_mapping(queryset, mapping, name, value, field):
    filter_values = mapping.get(value)
    if filter_values:
        filter_kwargs = {f"{field}__in": filter_values}
        return queryset.filter(**filter_kwargs)
    return queryset

def generate_choices(mapping):
    return [(key, key.capitalize()) for key in mapping.keys()]

FRAME_TYPE_MAPPING = {
    'magie': ['spell'],
    'piège': ['trap'],
    'monstre': [
        'normal',
        'effect',
        'ritual_pendulum',
        'effect_pendulum',
        'normal_pendulum',
        'ritual',
    ],
    'extra-deck': [
        'synchro',
        'synchro_pendulum',
        'fusion',
        'fusion_pendulum',
        'xyz',
        'xyz_pendulum',
        'link',
    ]
}

MONSTER_TYPE_MAPPING = {
    'normal': ['Normal Monster', 'Normal Tuner Monster', 'Pendulum Normal Monster'],
    'effet': ['Effect Monster'],
    'rituel': ['Ritual Effect Monster', 'Ritual Monster', 'Pendulum Effect Ritual Monster',],
    'fusion': ['Fusion Monster', 'Pendulum Effect Fusion Monster'],
    'synchro': [
        'Synchro Monster',
        'Synchro Pendulum Effect Monster',
        'Synchro Tuner Monster',
    ],
    'xyz': ['XYZ Monster', 'XYZ Pendulum Effect Monster'],
    'toon': ['Toon Monster'],
    'spirit': ['Spirit Monster'],
    'union': ['Union Effect Monster'],
    'gemini': ['Gemini Monster'],
    'syntoniseur': [
        'Normal Tuner Monster',
        'Flip Tuner Effect Monster',
        'Tuner Monster',
        'Synchro Tuner Monster',
        'Pendulum Tuner Effect Monster',
    ],
    'flip': ['Pendulum Flip Effect Monster', 'Flip Effect Monster', 'Flip Tuner Effect Monster'],
    'pendule': [
        'Pendulum Normal Monster',
        'Pendulum Effect Monster',
        'Pendulum Flip Effect Monster',
        'Pendulum Effect Ritual Monster',
        'Pendulum Effect Fusion Monster',
        'Pendulum Tuner Effect Monster',
        'Synchro Pendulum Effect Monster',
        'XYZ Pendulum Effect Monster',
    ],
    'lien': ['Link Monster'],
}



SPELL_TRAP_RACE_MAPPING = {
    'normal': ['Normal'],
    'continue': ['Continuous'],
    'terrain': ['Field'],
    'équipement': ['Equip'],
    'rituel': ['Ritual'],
    'rapide': ['Quick-Play'],
    'contre': ['Counter'],
}

MONSTER_RACE_MAPPING = {
    'aqua': ['Aqua'],
    'bête': ['Beast'],
    'bête-guerrier': ['Beast-Warrior'],
    'cyberse': ['Cyberse'],
    'dieu créateur': ['Creator God'],
    'dino': ['Dinosaur'],
    'bête-divine': ['Divine-Beast'],
    'dragon': ['Dragon'],
    'elfe': ['Fairy'],
    'démon': ['Fiend'],
    'poisson': ['Fish'],
    'insecte': ['Insect'],
    'machine': ['Machine'],
    'plante': ['Plant'],
    'psychique': ['Psychic'],
    'pyro': ['Pyro'],
    'reptile': ['Reptile'],
    'rocher': ['Rock'],
    'serpent de mer': ['Sea Serpent'],
    'magicien': ['Spellcaster'],
    'tonnerre': ['Thunder'],
    'guerrier': ['Warrior'],
    'bête ailée': ['Winged Beast'],
    'wyrm': ['Wyrm'],
    'zombie': ['Zombie'],
}

MONSTER_ATTRIBUTE_MAPPING = {
    'lumière': ['LIGHT'],
    'ténèbres': ['DARK'],
    'feu': ['FIRE'],
    'eau': ['WATER'],
    'terre': ['EARTH'],
    'vent': ['WIND'],
    'divin': ['DIVINE'],
}

FRAME_TYPE_CHOICES = generate_choices(FRAME_TYPE_MAPPING)
MONSTER_TYPE_CHOICES = generate_choices(MONSTER_TYPE_MAPPING)
SPELL_TRAP_RACE_CHOICES = generate_choices(SPELL_TRAP_RACE_MAPPING)
MONSTER_RACE_CHOICES = generate_choices(MONSTER_RACE_MAPPING)
MONSTER_ATTRIBUTE_CHOICES = generate_choices(MONSTER_ATTRIBUTE_MAPPING)