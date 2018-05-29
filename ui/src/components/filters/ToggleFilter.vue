<template>
    <div class="snow-toggle-filter">
        <div class="form-check">
            <label class="form-check-label">
                <input type="checkbox"
                       class="form-check-input"
                       v-model="checked">
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

        <div class="cutoff-date"
             v-if="default_date !== null && checked">
            <flat-pickr v-model="cutoff"
                        :config="dateConfig"/>
        </div>
    </div>
</template>

<style scoped>
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
                checked: null,
                cutoff: null,
                dateConfig: {
                    dateFormat: 'Y-m',
                    allowInput: true,
                },
            };
        },
        computed: {
            value() {
                // Treating criteria as exclusion criteria for the moment; will change with RS-18
                const filterValue = this.checked ? 0 : 1;

                if (this.default_date === null) {
                    return filterValue;
                }

                return {
                    value: filterValue,
                    date: dateToString(this.cutoff),
                };
            },
        },
        components: {
            FlatPickr,
        },
        mounted() {
            this.resetToDefault();

            // Initialize the description popover
            if (this.description) {
                $(this.$refs['description-link']).popover();
            }
        },
        methods: {
            setSelected(value) {
                this.checked = value;
            },
            resetToDefault() {
                this.cutoff = stringToDate(this.default_date);
                this.checked = this.default_value;
            },
        },
    };
</script>
