<template>
    <div class="snow-filter-panel">
        <h5>Filters</h5>

        <toggle-filter ref="toggle-filters"
                       v-for="filter in toggleFilters"
                       :key="filter.key"
                       :id="filter.key"
                       :label="filter.label"
                       :default_date="filter.default_date"
        />

        <distance-filter ref="ymca-filter"
                         id="ymca_fulton"
                         label="YMCA Fulton"/>

        <button type="submit"
                id="update-filters"
                @click="updateFilters"
                class="btn btn-primary">
            Update
        </button>
    </div>
</template>

<style scoped>
    .snow-filter-panel {
        padding-right: 1em;
        margin-right: 1em;
        border-right: 1px solid lightgrey;
    }

    #update-filters {
        margin-top: 1em;
    }
</style>

<script>
    import _ from 'lodash';

    import { mapGetters } from 'vuex';
    import ToggleFilter from './filters/ToggleFilter';
    import DistanceFilter from './filters/DistanceFilter';


    function flattenToDotNotation(filters) {
        return _.merge(..._.map(filters, (value, key) => {
            if (typeof value === 'object') {
                return _.mapKeys(value, (subvalue, subkey) => `${key}.${subkey}`);
            }

            return _.fromPairs([[key, value]]);
        }));
    }

    export default {
        name: 'FilterPanel',
        components: {
            ToggleFilter,
            DistanceFilter,
        },
        methods: {
            updateFilters() {
                const filters = flattenToDotNotation(this.filterValues);

                // TODO: Replace with a more graceful way of including distance filters
                const ymcaValue = this.ymcaFilter;
                if (ymcaValue !== null) {
                    filters.ymca_fulton = ymcaValue;
                }

                this.$store.dispatch('getFilteredStats', filters);
            },
        },
        computed: {
            ...mapGetters(['modelFilters']),
            toggleFilters() {
                return _.filter(this.modelFilters, o => o.type === 'toggle');
            },
            filterValues() {
                const activeFilters = _.keyBy(_.filter(this.$refs['toggle-filters'], f => f.checked), 'id');
                return _.mapValues(activeFilters, f => f.value);
            },
            ymcaFilter() {
                const ymcaFilter = this.$refs['ymca-filter'];
                return ymcaFilter.value;
            },
        },
        mounted() {
            this.$store.dispatch('getCriteriaDataModel');
        },
    };
</script>
