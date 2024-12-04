<template>
    <div class="container">
        <filter-form :filters="filters" @apply-filters="applyFilters" @reset-filters="resetFilters"></filter-form>
        <app-pagination v-if="!loading && pagination.totalPages > 1"
            :current-page="pagination.currentPage"
            :total-pages="pagination.totalPages"
            :total-cards="pagination.totalCards"
            @change-page="fetchCards"
        ></app-pagination>
        <card-list :cards="cards" :loading="loading"></card-list>
        <app-pagination v-if="!loading && pagination.totalPages > 1"
            :current-page="pagination.currentPage"
            :total-pages="pagination.totalPages"
            :total-cards="pagination.totalCards"
            @change-page="fetchCards"
        ></app-pagination>
    </div>
</template>

<script>
import FilterForm from '@/components/FilterForm.vue';
import CardList from '@/components/CardList.vue';
import AppPagination from '@/components/AppPagination.vue';

export default {
    components: { FilterForm, CardList, AppPagination },
    data() {
        return {
            filters: {
                name: '',
                frame_type: '',
                spell_trap_race: '',
                type: '',
                monster_race: '',
                attribute: '',
                attackMin: '',
                attackMax: '',
                defenseMin: '',
                defenseMax: '',
                levelMin: '',
                levelMax: '',
                limit: 20,
            },
            cards: [],
            pagination: { currentPage: 1, totalPages: 0, totalCards: 20 },
            loading: false,
        };
    },
    methods: {
        fetchCards(page = 1) {
            this.loading = true;
            const queryParams = new URLSearchParams({
                name: this.filters.name,
                frame_type: this.filters.frame_type,
                spell_trap_race: this.filters.spell_trap_race,
                type: this.filters.type,
                monster_race: this.filters.monster_race,
                attribute: this.filters.attribute,
                attack_min: this.filters.attackMin,
                attack_max: this.filters.attackMax,
                defense_min: this.filters.defenseMin,
                defense_max: this.filters.defenseMax,
                level_rank_min: this.filters.levelMin,
                level_rank_max: this.filters.levelMax,
                limit: this.filters.limit,
                page,
                json: 'true',
            }).toString();
            fetch(`http://localhost:8000/api/card/?${queryParams}`, {
                method: 'GET',
                headers: {
                    'Accept': 'application/json',
                    'x-requested-with': 'XMLHttpRequest',  // Indicate AJAX request
                },
            })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                    this.cards = data.items;
                    this.pagination = {
                        currentPage: data.pagination.current_page,
                        totalPages: data.pagination.total_pages,
                        totalCards: data.pagination.total_items,
                    };
                    this.loading = false
                })
                .catch(error => {
                    console.error("Erreur dans la récupération des données:", error);
                    this.loading = false
                });
        },
        applyFilters(filters) {
            this.filters = { ...filters };
            this.fetchCards(1);
        },
        resetFilters() {
            this.filters = {
                name: '',
                frame_type: '',
                spell_trap_race: '',
                type: '',
                monster_race: '',
                attribute: '',
                attackMin: '',
                attackMax: '',
                defenseMin: '',
                defenseMax: '',
                levelMin: '',
                levelMax: '',
                limit: this.filters.limit,
            };
            this.fetchCards(1);
        }
    },
    created() {
        this.fetchCards();
    }
};
</script>