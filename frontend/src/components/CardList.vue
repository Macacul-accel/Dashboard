<template>
    <div v-if="loading" class="loader">Chargement en cours...</div>
    <div v-else>
        <div v-if="cards" class="card-container border rounded">
            <div v-for="card in cards" :key="card.id" class="border d-flex px-2 py-2">
                <div class="mx-3 my-3">
                    <img :src="card.image" :alt="card.name" loading="lazy" width="270" height="370">
                </div>
                
                <div class="card-content d-flex px-3 py-3 flex-column">
                    <div class="p-3 text-center" style="height: 64px; width: 762px;">
                        <h5>{{ card.name }}</h5>
                    </div>
                    
                    <div class="text-center" style="height: 160px; width: 762px">
                        <div class="d-flex justify-content-between mx-5" style="height: 50px; width: 600px;">
                            <span>{{ card.type }}</span>
                            <span v-if="card.type === 'Trap Card' || card.type === 'Spell Card'">{{ card.spell_trap_race }}</span>
                            <span v-else>{{ card.monster_race }}</span>
                            <span v-if="card.attribute">{{ card.attribute }}</span>
                        </div>
                        <p v-if="card.level_rank">LVL: {{ card.level_rank }}</p>
                        <p v-if="card.attack">ATK: {{ card.attack }}</p>
                        <p v-if="card.defense">DEF: {{ card.defense }}</p>
                    </div>
                    
                    <p>{{ card.effect }}</p>
                </div>
            </div>
        </div>
        
        <p v-else>Aucune carte ne correspond à ce filtre.</p>
    </div>
</template>


<script>
export default {
    props: ['cards', 'loading'],
};
</script>
