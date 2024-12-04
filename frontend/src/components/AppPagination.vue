<template>
    <div class="pagination justify-content-center align-items-center py-3 mt-4">
        <button :disabled="!hasPrevious" @click="$emit('change-page', currentPage - 1)" class="page-link rounded px-3">
            &lsaquo; Précédent
        </button>
        <span class="px-2">Page {{ currentPage }} / {{ totalPages }} sur {{ totalCards }} cartes</span>
        <button :disabled="!hasNext" @click="$emit('change-page', currentPage + 1)" class="page-link rounded px-3">
            Suivant &rsaquo;
        </button>
    </div>
</template>

<script>
export default {
    props: ['currentPage', 'totalPages', 'totalCards'],
    computed: {
        hasPrevious() {
            return this.currentPage > 1;
        },
        hasNext() {
            return this.currentPage < this.totalPages;
        }
    }
};
</script>
