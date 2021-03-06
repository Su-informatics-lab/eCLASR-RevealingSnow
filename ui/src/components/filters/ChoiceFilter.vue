<template>
    <div class="snow-choice-filter">
        <div class="form-check">
            <label class="form-check-label"
                   for="choice">
                <input type="checkbox"
                       class="form-check-input"
                       v-model="enabled">
                {{ label }}
            </label>

            <a ref="description-link"
               tabindex="0"
               role="button"
               class="snow-filter-help"
               data-trigger="focus"
               data-toggle="popover"
               v-if="description"
               :data-content="description">
                <sup>?</sup>
            </a>
        </div>

        <div class="snow-choice-value"
             v-if="enabled">
            <select
                multiple
                id="choice"
                class="form-control"
                v-model="selections">
                <option
                    v-for="value in allowedValues"
                    :value="value.key"
                    :key="value.key"
                    :id="value.key">{{ value.label }}
                </option>
            </select>
        </div>
    </div>
</template>

<style scoped>
.snow-choice-filter {
    padding-left: 0.5em;
    padding-top: 0.25em;
    padding-bottom: 0.25em;
}

.snow-choice-value {
    padding-left: 2em;
}

.snow-choice-value > select {
    font-size: inherit;
}

.snow-filter-help {
    font-size: xx-small;
    font-weight: bold;
    cursor: pointer;
}
</style>

<script>
import _ from 'lodash';
import $ from 'jquery';


export default {
    name: 'ChoiceFilter',
    props: {
        id: {
            type: String,
            required: true,
        },
        label: {
            type: String,
            required: true,
        },
        default_value: {
            type: Boolean,
            default: false,
        },
        allowedValues: {
            type: Array,
            default: null,
        },
        description: {
            type: String,
            default: '',
        },
    },
    data() {
        return {
            enabled: false,
            selections: [],
        };
    },
    computed: {
        value() {
            if (this.enabled === false) {
                return null;
            }

            if (this.selections.length === 0) {
                return null;
            }

            return _.join(this.selections, ',');
        },
    },
    mounted() {
        this.resetToDefault();

        // Initialize the description popover
        if (this.description) {
            $(this.$refs['description-link']).popover();
        }
    },
    watch: {
        enabled() {
            this.$emit('updated');
        },
        selections() {
            this.$emit('updated');
        },
    },
    methods: {
        setEnabled(value) {
            this.enabled = value;
        },
        resetToDefault() {
            this.enabled = this.default_value;
        },
        set(value) {
            this.setEnabled(true);
            this.selections = value;
        },
    },
};
</script>
