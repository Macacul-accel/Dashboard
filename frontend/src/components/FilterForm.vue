<template>
    <form @change.prevent="applyFilters">
        <div class="form-group">
            <input type="search" v-model="localFilters.name" placeholder="Rechercher par nom" class="form-control">
        </div>
        <div>
            <label>Type de carte :</label>
            <select v-model="localFilters.frame_type" class="form-select">
                <option value="">Tous</option>
                <option value="magie">Magie</option>
                <option value="piège">Piège</option>
                <option value="monstre">Monstre</option>
                <option value="extra-deck">Extra-deck</option>
            </select>
        </div>
        <div>
            <label>Type de magie, piège :</label>
            <select v-model="localFilters.spell_trap_race" class="form-select">
                <option value="" selected>Tous</option>
                <option value="normal">Normal</option>
                <option value="continue">Continue</option>
                <option value="terrain">Terrain</option>
                <option value="équipement">Équipement</option>
                <option value="rituel">Rituel</option>
                <option value="rapide">Rapide</option>
                <option value="contre">Contre</option>
            </select>
        </div>
        <div>
            <label>Autre :</label> 
            <select v-model="localFilters.type" class="form-select">
                <option value="">Tous</option>
                <option value="normal">Normal</option>
                <option value="effet">Effet</option>
                <option value="rituel">Rituel</option>
                <option value="fusion">Fusion</option>
                <option value="synchro">Synchro</option>
                <option value="xyz">Xyz</option>
                <option value="toon">Toon</option>
                <option value="spirit">Spirit</option>
                <option value="union">Union</option>
                <option value="gemini">Gemini</option>
                <option value="syntoniseur">Syntoniseur</option>
                <option value="flip">Flip</option>
                <option value="pendule">Pendule</option>
                <option value="lien">Lien</option>
            </select>
        </div>
        <div>
            <label>Type de monstre :</label>
            <select v-model="localFilters.monster_race" class="form-select">
                <option value="">Tous</option>
                <option value="aqua">Aqua</option>
                <option value="bête">Bête</option>
                <option value="bête-guerrier">Bête-guerrier</option>
                <option value="cyberse">Cyberse</option>
                <option value="dieu créateur">Dieu créateur</option>
                <option value="dino">Dino</option>
                <option value="bête-divine">Bête-divine</option>
                <option value="dragon">Dragon</option>
                <option value="elfe">Elfe</option>
                <option value="démon">Démon</option>
                <option value="poisson">Poisson</option>
                <option value="insecte">Insecte</option>
                <option value="machine">Machine</option>
                <option value="plante">Plante</option>
                <option value="psychique">Psychique</option>
                <option value="pyro">Pyro</option>
                <option value="reptile">Reptile</option>
                <option value="rocher">Rocher</option>
                <option value="serpent de mer">Serpent de mer</option>
                <option value="magicien">Magicien</option>
                <option value="tonnerre">Tonnerre</option>
                <option value="guerrier">Guerrier</option>
                <option value="bête ailée">Bête ailée</option>
                <option value="wyrm">Wyrm</option>
                <option value="zombie">Zombie</option>
            </select>
        </div>
        <div>
            <label>Attribut :</label>
            <select v-model="localFilters.attribute" class="form-select">
                <option value="">Tous</option>
                <option value="lumière">Lumière</option>
                <option value="ténèbres">Ténèbres</option>
                <option value="feu">Feu</option>
                <option value="eau">Eau</option>
                <option value="terre">Terre</option>
                <option value="vent">Vent</option>
                <option value="divin">Divin</option>
            </select>
        </div>
        <div>
            <label>Attaque :</label>
            <input type="range" v-model="localFilters.attackMin" :min="0" :max="5000" step="50">
            <span>{{ localFilters.attackMin }}</span>
            <input type="range" v-model="localFilters.attackMax" :min="0" :max="5000" step="50">
            <span>{{ localFilters.attackMax }}</span>
        </div>
        <div>
            <label>Défense :</label>
            <input type="range" v-model="localFilters.defenseMin" :min="0" :max="5000" step="50">
            <span>{{ localFilters.defenseMin }}</span>
            <input type="range" v-model="localFilters.defenseMax" :min="0" :max="5000" step="50">
            <span>{{ localFilters.defenseMax }}</span>
        </div>
        <div>
            <label>Niveau/Rang :</label>
            <input type="range" v-model="localFilters.levelMin" :min="1" :max="13" step="1">
            <span>{{ localFilters.levelMin }}</span>
            <input type="range" v-model="localFilters.levelMax" :min="1" :max="13" step="1">
            <span>{{ localFilters.levelMax }}</span>
        </div>
        
        <button type="button" @click="resetFilters" class="btn btn-danger">Effacer tous les filtres</button>
    </form>
</template>

<script>
export default {
    props: ['filters'],
    data() {
        return {
            // Create a local copy of the filters prop to avoid directly mutating it
            localFilters: { ...this.filters } // Using spread syntax to copy the filters object
        };
    },
    watch: {
        // Watch for changes to the filters prop and update localFilters when it changes
        filters(newFilters) {
            this.localFilters = { ...newFilters }; // Update the local copy of the filters
        }
    },
    methods: {
        applyFilters() {
            this.$emit('apply-filters', this.localFilters);
        },
        resetFilters() {
            this.localFilters = { ...this.filters};
            this.$emit('reset-filters');
        }
    }
};
</script>
