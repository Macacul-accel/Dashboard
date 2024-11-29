<template>
    <div class="pagination">
        <button :disabled="!hasPrevious" @click="$emit('change-page', currentPage - 1)">
            &lsaquo; Précédent
        </button>
        <span>Page {{ currentPage }} sur {{ totalPages }}</span>
        <button :disabled="!hasNext" @click="$emit('change-page', currentPage + 1)">
            Suivant &rsaquo;
        </button>
    </div>
</template>

<script>
export default {
    props: ['currentPage', 'totalPages'],
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
