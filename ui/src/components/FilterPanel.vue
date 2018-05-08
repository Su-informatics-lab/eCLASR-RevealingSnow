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
        },
        methods: {
            updateFilters() {
                const filters = flattenToDotNotation(this.filterValues);
                this.$store.dispatch('getPatientStats', filters);
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
        },
        mounted() {
            this.$store.dispatch('getCriteriaDataModel');
        },
    };
</script>
