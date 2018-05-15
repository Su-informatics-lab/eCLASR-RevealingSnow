<template>
    <div class="snow-distance-filter">
        <div class="form-check">
            <label class="form-check-label">
                <input type="checkbox"
                       class="form-check-input"
                       v-model="enabled">
                {{ label }}
            </label>
        </div>

        <div class="snow-distance-filter-controls"
             v-if="enabled">
            <div class="form-row">
                <label>
                    Max ({{ maxValue }}):
                    <input type="range"
                           v-model="maxValue">
                </label>
            </div>
        </div>
    </div>
</template>

<style scoped>
    .snow-distance-filter-controls {
        padding-left: 1em;
    }
</style>

<script>
    export default {
        name: 'DistanceFilter',
        props: {
            id: {
                type: String,
                required: true,
            },
            label: {
                type: String,
                required: true,
            },
        },
        data() {
            return {
                enabled: false,
                maxValue: 5,
                distance: '5',
            };
        },
        computed: {
            value() {
                if (this.distance === '-1') {
                    return null;
                }

                return this.distance;
            },
        },
    };
</script>
