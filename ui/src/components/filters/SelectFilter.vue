<template>
    <div class="snow-select-filter">
        <div class="snow-select-control">
            <label class="form-check-label">
                <ternary-toggle v-model="state"
                                :enabled="enabled"/>

                <span> {{ label }} </span>
            </label>
        </div>

        <div class="snow-select-value"
             v-if="state !== null">
            <select
                id="select"
                class="form-control">
                <option>Foo</option>
            </select>
        </div>
    </div>
</template>

<style scoped>
    .snow-select-filter {
        padding-top: 0.25em;
        padding-bottom: 0.25em;
    }

    .snow-select-control {
        padding-left: 0.5em;
    }

    .snow-select-value {
        padding-left: 2em;
    }

    .snow-select-value > select {
        font-size: inherit;
    }
</style>

<script>
    import TernaryToggle from './TernaryToggle';


    export default {
        name: 'SelectFilter',
        props: {
            id: {
                type: String,
                required: true,
            },
            label: {
                type: String,
                required: true,
            },
            enabled: {
                type: Boolean,
                default: true,
            },
            default_value: {
                type: Boolean,
                default: null,
            },
        },
        data() {
            return {
                state: null,
                selection: null,
            };
        },
        mounted() {
            this.resetToDefault();
        },
        methods: {
            resetToDefault() {
                this.state = this.default_value;
            }
        },
        components: {
            TernaryToggle,
        },
    };
</script>
