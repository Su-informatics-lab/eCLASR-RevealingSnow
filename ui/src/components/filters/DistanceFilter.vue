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
                    <input title="Minimum Distance Input"
                           type="number"
                           v-model="minValue"
                           :min="minDistance"
                           :max="maxValue"
                           class="snow-distance-filter-text-input">
                </div>
                <div class="col-2">
                    to
                </div>
                <div class="col">
                    <input title="Maximum Distance Input"
                           type="number"
                           v-model="maxValue"
                           :min="minValue"
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
        width: 100%;
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
                minValue: 0,
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
                    maxdist: this.maxValue,
                    mindist: this.minValue,
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
            minValue() {
                this.$emit('updated');
            },
        },
        methods: {
            setSelected(value) {
                this.enabled = value;
            },
            setMaxdist(value) {
                this.maxValue = value;
            },
            setMindist(value) {
                this.minValue = value;
            },
        },
    };
</script>
