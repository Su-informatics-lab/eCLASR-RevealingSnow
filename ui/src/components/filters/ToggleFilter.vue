<template>
    <div class="snow-toggle-filter">
        <div class="snow-toggle-control">
            <label class="form-check-label">
                <ternary-toggle v-model="state"/>

                <span> {{ label }} </span>
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

        <div class="cutoff-date"
             v-if="default_date !== null && state !== null">
            <flat-pickr v-model="cutoff"
                        :config="dateConfig"/>
        </div>
    </div>
</template>

<style scoped>
    .snow-toggle-filter {
        padding-top: 0.25em;
        padding-bottom: 0.25em;
    }

    .snow-toggle-control {
        padding-left: 0.5em;
    }

    .cutoff-date {
        padding-left: 2em;
    }

    .cutoff-date > input {
        width: 100%;
    }

    .form-check-label {
        display: inline;
    }

    .snow-filter-help {
        font-size: xx-small;
        font-weight: bold;
        cursor: pointer;
    }
</style>

<script>
    import $ from 'jquery';

    import FlatPickr from 'vue-flatpickr-component';
    import 'flatpickr/dist/flatpickr.css';

    import moment from 'moment';

    import TernaryToggle from './TernaryToggle';


    function stringToDate(value) {
        return moment(value).toDate();
    }

    function dateToString(value) {
        return moment(value).format('YYYY-MM-DD');
    }


    export default {
        name: 'ToggleFilter',
        props: {
            id: {
                type: String,
                required: true,
            },
            label: {
                type: String,
                required: true,
            },
            default_date: {
                type: String,
                default: null,
            },
            default_value: {
                type: Boolean,
                default: null,
            },
            description: {
                type: String,
                default: '',
            },
        },
        data() {
            return {
                state: null,
                cutoff: null,
                dateConfig: {
                    dateFormat: 'Y-m-d',
                    allowInput: true,
                },
            };
        },
        computed: {
            value() {
                if (this.state === null) {
                    return null;
                }

                const filterValue = this.state ? 1 : 0;

                if (this.default_date === null) {
                    return filterValue;
                }

                return {
                    value: filterValue,
                    date: dateToString(this.cutoff),
                };
            },
            checked() {
                return this.state !== null;
            },
        },
        components: {
            FlatPickr,
            TernaryToggle,
        },
        mounted() {
            this.resetToDefault();

            // Initialize the description popover
            if (this.description) {
                $(this.$refs['description-link']).popover();
            }
        },
        watch: {
            state() {
                this.$emit('updated');
            },
            cutoff() {
                this.$emit('updated');
            },
        },
        methods: {
            setSelected(value) {
                this.state = value;
            },
            setCutoff(value) {
                this.cutoff = value;
            },
            set(value) {
                if (this.default_date === null) {
                    this.setSelected(value);
                } else {
                    this.setSelected(value.value);
                    this.setCutoff(value.date);
                }
            },
            resetToDefault() {
                this.cutoff = stringToDate(this.default_date);
                this.state = this.default_value;
            },
        },
    };
</script>
