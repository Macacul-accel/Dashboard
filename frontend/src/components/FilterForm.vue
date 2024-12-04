<template>
    <div class="pt-5">
        <h1 class="my-5">Liste des cartes</h1>
        <form @change.prevent="applyFilters">
            <div class="form-group d-flex align-items-center position relative">
                <input type="search" v-model="localFilters.name" placeholder="Rechercher par nom" class="form-control form-control-lg">
            </div>
            <div class="toggle-buttons d-flex justify-content-center py-5">
                <a class="filter-button text-center" data-bs-toggle="collapse"
                data-bs-target="#toggleSearchFilters" aria-expanded="false" aria-controls="toggleSearchFilters">
                    <i class="bi bi-filter"></i>
                </a>
                <div class="form-group px-5">
                    <label>Cartes par page:</label>
                    <select v-model="localFilters.limit" class="form-select">
                        <option :value="20">20</option>
                        <option :value="50">50</option>
                        <option :value="75">75</option>
                        <option :value="100">100</option>
                    </select>
                </div>
            </div>
            <div class="p-3 border rounded collapse" id="toggleSearchFilters">
                <div class="d-flex justify-content-center flex-wrap">
                    <div class="form-group py-3 px-4">
                    <label>Type de carte :</label>
                    <select v-model="localFilters.frame_type" class="form-select">
                        <option value="">Tous</option>
                        <option value="magie">Magie</option>
                        <option value="piège">Piège</option>
                        <option value="monstre">Monstre</option>
                        <option value="extra-deck">Extra-deck</option>
                    </select>
                    </div>
                    <div class="form-group py-3 px-4">
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
                    <div class="form-group py-3 px-4">
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
                    <div class="form-group py-3 px-4">
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
                    <div class="form-group py-3 px-4">
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
                    <div class="form-group py-3 px-4">
                        <label>Attaque :</label>
                        <input class="range-slider" type="range" v-model="localFilters.attackMin" :min="0" :max="5000" step="50">
                        <span>{{ localFilters.attackMin }}</span>
                        <input class="range-slider" type="range" v-model="localFilters.attackMax" :min="0" :max="5000" step="50">
                        <span>{{ localFilters.attackMax }}</span>
                    </div>
                    <div class="form-group py-3 px-4">
                        <label>Défense :</label>
                        <input class="range-slider" type="range" v-model="localFilters.defenseMin" :min="0" :max="5000" step="50">
                        <span>{{ localFilters.defenseMin }}</span>
                        <input class="range-slider" type="range" v-model="localFilters.defenseMax" :min="0" :max="5000" step="50">
                        <span>{{ localFilters.defenseMax }}</span>
                    </div>
                    <div class="form-group py-3 px-4">
                        <label>Niveau/Rang :</label>
                        <input class="range-slider" type="range" v-model="localFilters.levelMin" :min="1" :max="13" step="1">
                        <span>{{ localFilters.levelMin }}</span>
                        <input class="range-slider" type="range" v-model="localFilters.levelMax" :min="1" :max="13" step="1">
                        <span>{{ localFilters.levelMax }}</span>
                    </div>
                </div>
                <div class="d-flex justify-content-center py-4">
                    <button type="button" @click="resetFilters" class="btn btn-danger">Effacer tous les filtres</button>
                </div>
            </div>
        </form>
    </div>
</template>

<script>
export default {
    props: ['filters'],
    data() {
        return {
            // Create a local copy of the filters prop to avoid directly mutating it
            localFilters: { ...this.filters, limit: 20 },// Using spread syntax to copy the filters object and the default limit
        };
    },
    watch: {
        // Watch for changes to the filters prop and update localFilters when it changes
        filters(newFilters) {
            this.localFilters = { ...newFilters, limit: this.localFilters.limit }; // Update the local copy of the filters
        }
    },
    methods: {
        applyFilters() {
            this.$emit('apply-filters', this.localFilters); // Emit the updated filters with the limit
        },
        resetFilters() {
            this.localFilters = { ...this.filters, limit: this.localFilters.limit }; // Keep the current limit
            this.$emit('reset-filters');
        }
    }
};
</script>
