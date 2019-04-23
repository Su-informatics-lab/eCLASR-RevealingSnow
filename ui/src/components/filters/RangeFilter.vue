<template>
    <div class="snow-range-filter">
        <div class="form-check">
            <label class="form-check-label">
                <input type="checkbox"
                       class="form-check-input"
                       v-model="enabled">
                {{ label }}
            </label>
        </div>

        <div class="snow-range-filter-controls"
             v-if="enabled">
            <input type="number"
                   placeholder="Min"
                   :min="minValue"
                   :max="selectedMaximum || maxValue"
                   v-model="selectedMinimum">

            <input type="number"
                   placeholder="Max"
                   :min="selectedMinimum || minValue"
                   :max="maxValue"
                   v-model="selectedMaximum">
        </div>
    </div>
</template>

<style scoped>
    .snow-range-filter {
        padding-left: 0.5em;
        padding-top: 0.25em;
        padding-bottom: 0.25em;
    }

    .snow-range-filter-controls {
        padding-left: 1.5em;
    }

    .snow-range-filter-controls > input {
        min-width: 4em;
    }
</style>

<script>
    import _ from 'lodash';


    export default {
        name: 'RangeFilter',
        props: {
            id: {
                type: String,
                required: true,
            },
            label: {
                type: String,
                required: true,
            },
            minValue: {
                type: Number,
                default: 1,
            },
            maxValue: {
                type: Number,
                default: 100,
            },
        },
        data() {
            return {
                enabled: false,
                selectedMinimum: null,
                selectedMaximum: null,
            };
        },
        computed: {
            value() {
                if (this.enabled === false) {
                    return null;
                }

                const range = {
                    min: this.selectedMinimumValue,
                    max: this.selectedMaximumValue,
                };

                return _.pickBy(range, _.isNumber);
            },
            selectedMinimumValue() {
                return this.getNullOrInt(this.selectedMinimum);
            },
            selectedMaximumValue() {
                return this.getNullOrInt(this.selectedMaximum);
            },
        },
        watch: {
            enabled() {
                this.$emit('updated');
            },
            selectedMinimum() {
                this.$emit('updated');
            },
            selectedMaximum() {
                this.$emit('updated');
            },
        },
        methods: {
            setEnabled(value) {
                this.enabled = value;
            },
            setMinimumValue(value) {
                this.selectedMinimum = value;
            },
            setMaximumValue(value) {
                this.selectedMaximum = value;
            },
            resetToDefault() {
                this.enabled = false;
                this.selectedMinimum = null;
                this.selectedMaximum = null;
            },
            getNullOrInt(value) {
                if (_.isEmpty(value)) {
                    return null;
                }

                return _.toNumber(value);
            },
            set(value) {
                this.setEnabled(true);
                this.setMinimumValue(_.get(value, 'min', null));
                this.setMaximumValue(_.get(value, 'max', null));
            },
        },
    };
</script>
