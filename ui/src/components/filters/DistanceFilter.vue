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
                <div class="col">
                    <input title="Maximum Distance Slider"
                           type="range"
                           v-model="maxValue"
                           :min="minDistance"
                           :max="maxDistance"
                           class="snow-distance-filter-slider-input">
                </div>
                <div class="col">
                    <input title="Maximum Distance Input"
                           type="number"
                           v-model="maxValue"
                           :min="minDistance"
                           :max="maxDistance"
                           class="snow-distance-filter-text-input">
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
    .snow-distance-filter-controls {
        padding-left: 1em;
    }

    .snow-distance-filter-text-input {
        width: 3em;
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
            minDistance: {
                type: Number,
                default: 1,
            },
            maxDistance: {
                type: Number,
                default: 100,
            },
        },
        data() {
            return {
                enabled: false,
                maxValue: 15,
            };
        },
        computed: {
            value() {
                if (this.maxValue === 0) {
                    return null;
                }

                return {
                    site: this.id,
                    cutoff: this.maxValue,
                };
            },
        },
        watch: {
            enabled() {
                this.$emit('updated');
            },
            maxValue() {
                this.$emit('updated');
            },
        },
        methods: {
            setSelected(value) {
                this.enabled = value;
            },
        },
    };
</script>
