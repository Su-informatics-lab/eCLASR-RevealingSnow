<template>
    <div class="filters">
        <h5>Filters</h5>

        <div class="form-check">
            <label class="form-check-label">
                <input type="checkbox"
                       class="form-check-input"
                       v-model="cardiac">

                Cardiac
            </label>
        </div>

        <div class="form-check">
            <label class="form-check-label">
                <input type="checkbox"
                       class="form-check-input"
                       v-model="neuro">

                Neuro
            </label>
        </div>

        <button type="submit"
                id="update-filters"
                @click="updateFilters"
                class="btn btn-primary">
            Update
        </button>
    </div>
</template>

<style scoped>
    .filters {
        text-align: left;
    }

    #update-filters {
        margin-top: 1em;
    }
</style>

<script>
    import _ from 'lodash';


    export default {
        name: 'Filters',
        data() {
            return {
                cardiac: false,
                neuro: false,
            };
        },
        methods: {
            updateFilters() {
                const filters = {
                    cardiac: this.cardiac ? 1 : 0,
                    neuro: this.neuro ? 1 : 0,
                };

                this.$store.dispatch('getPatientStats', _.pickBy(filters, x => x === 1));
            },
        },
    };
</script>
