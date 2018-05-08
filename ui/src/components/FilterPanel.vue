<template>
    <div class="snow-filter-panel">
        <h5>Filters</h5>

        <toggle-filter ref="toggle-filters"
                       v-for="filter in toggleFilters"
                       :key="filter.key"
                       :id="filter.key"
                       :label="filter.label"/>

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

    import { mapGetters } from 'vuex';
    import ToggleFilter from './filters/ToggleFilter';


    export default {
        name: 'FilterPanel',
        components: {
            ToggleFilter,
        },
        methods: {
            updateFilters() {
                const filters = this.filterValues;
                this.$store.dispatch('getPatientStats', filters);
            },
        },
        computed: {
            ...mapGetters(['modelFilters']),
            toggleFilters() {
                return _.filter(this.modelFilters, o => o.type === 'toggle');
            },
            filterValues() {
                const activeFilters = _.keyBy(_.filter(this.$refs['toggle-filters'], f => f.value), 'id');
                return _.mapValues(activeFilters, () => 0);
            },
        },
        mounted() {
            this.$store.dispatch('getCriteriaDataModel');
        },
    };
</script>
