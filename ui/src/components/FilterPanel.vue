<template>
    <div class="snow-filter-panel">
        <h5>Filters</h5>

        <toggle-filter ref="cardiac"
                       label="Cardiac"/>
        <toggle-filter ref="neuro"
                       label="Neuro"/>

        <button type="submit"
                id="update-filters"
                @click="updateFilters"
                class="btn btn-primary">
            Update
        </button>
    </div>
</template>

<style scoped>

</style>

<script>
    import _ from 'lodash';
    import ToggleFilter from './filters/ToggleFilter';


    export default {
        name: 'FilterPanel',
        components: {
            ToggleFilter,
        },
        methods: {
            updateFilters() {
                const filters = {
                    cardiac: this.$refs.cardiac.value ? 0 : 1,
                    neuro: this.$refs.neuro.value ? 0 : 1,
                };

                this.$store.dispatch('getPatientStats', _.pickBy(filters, x => x === 0));
            },
        },
    };
</script>
