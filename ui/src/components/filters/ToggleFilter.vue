<template>
    <div class="snow-toggle-filter">
        <div class="form-check">
            <label class="form-check-label">
                <input type="checkbox"
                       class="form-check-input"
                       v-model="checked">
                {{ label }}
            </label>
        </div>

        <div class="cutoff-date"
             v-if="default_date !== null && checked">
            <vue-date-picker v-model="cutoff"
                             format="yyyy-MM"
                             minimum-view="month"
            />
        </div>
    </div>
</template>

<style scoped>
    .cutoff-date {
        padding-left: 2em;
    }
</style>

<script>
    import VueDatePicker from 'vuejs-datepicker';
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
        },
        data() {
            return {
                checked: null,
                cutoff: null,
            };
        },
        computed: {
            value() {
                // Treating filters as exclusion criteria for the moment; will change with RS-18
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
            VueDatePicker,
        },
        mounted() {
            this.cutoff = stringToDate(this.default_date);
        },
    };
</script>
