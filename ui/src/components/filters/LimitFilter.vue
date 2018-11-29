<template>
    <div class="snow-limit-filter">
        <div class="form-check">
            <label class="form-check-label">
                <input type="checkbox"
                       class="form-check-input"
                       v-model="enabled">
                {{ label }}
            </label>
        </div>

        <div class="snow-limit-filter-controls"
             v-if="enabled">
            <input type="number"
                   v-model="limitCount"
                   min="1"
                   :max="maxLimitCount">

            <span>
                ordered by
            </span>

            <select v-model="orderColumn">
                <option value="last_visit_date">Visit Date</option>
                <option value="closest_ymca">Closest YMCA Site</option>
            </select>

            <select v-model="orderAscending">
                <option :value="false">Descending</option>
                <option :value="true">Ascending</option>
            </select>
        </div>
    </div>
</template>

<style scoped>
    .snow-limit-filter {
        padding-left: 0.5em;
    }

    .snow-limit-filter-controls {
        padding-left: 1em;
    }

</style>

<script>
    export default {
        name: 'LimitFilter',
        props: {
            id: {
                type: String,
                required: true,
            },
            label: {
                type: String,
                required: true,
            },
            maxLimitCount: {
                type: Number,
                default: 1000,
            },
        },
        data() {
            return {
                enabled: false,
                limitCount: 1000,
                orderColumn: 'last_visit_date',
                orderAscending: false,
            };
        },
        computed: {
            value() {
                if (this.enabled === false) {
                    return null;
                }

                return {
                    limit: this.limitCount,
                    order_by: this.orderColumn,
                    order_asc: this.orderAscending,
                };
            },
        },
        watch: {
            enabled() {
                this.$emit('updated');
            },
            limitCount() {
                this.$emit('updated');
            },
            orderColumn() {
                this.$emit('updated');
            },
            orderAscending() {
                this.$emit('updated');
            },
        },
    };
</script>
