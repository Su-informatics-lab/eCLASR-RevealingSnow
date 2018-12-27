<template>
    <div class="snow-export-form">
        <div class="form-group">
            <input type="text"
                   class="form-control"
                   placeholder="Your Name (Optional)"
                   v-model="exportUsername">
        </div>

        <div class="form-group">
            <input type="text"
                   class="form-control"
                   placeholder="Label (Optional)"
                   v-model="exportLabel">
        </div>

        <div class="form-group">
            <textarea class="form-control"
                      placeholder="Description (Optional)"
                      rows="3"
                      v-model="exportDescription"/>
        </div>

        <div class="form-check">
            <input class="form-check-input"
                   type="radio"
                   id="export-all"
                   value="all"
                   v-model="exportMode">
            <label class="form-check-label"
                   for="export-all">
                Export all matching patients
            </label>
        </div>

        <div class="form-check">
            <input class="form-check-input"
                   type="radio"
                   id="export-subset"
                   value="subset"
                   v-model="exportMode">
            <label class="form-check-label"
                   for="export-subset">
                Export a subset
            </label>
        </div>

        <div class="snow-subset-options row">
            <input type="number"
                   v-model="exportCount"
                   min="1"
                   :max="maxExportCount"
                   :disabled="!isSubsetSelected">

            <span>
                ordered by
            </span>

            <select v-model="orderColumn"
                    :disabled="!isSubsetSelected">
                <option value="last_visit_date">Visit Date</option>
                <option value="closest_ymca">Closest YMCA Site</option>
            </select>

            <select v-model="orderAscending"
                    :disabled="!isSubsetSelected">
                <option :value="false">Descending</option>
                <option :value="true">Ascending</option>
            </select>
        </div>
    </div>
</template>

<style scoped>
    .snow-export-form {
        text-align: left;
    }

    .snow-subset-options {
        margin-left: 1em;
    }

    .snow-subset-options > input, span, select {
        margin-left: 0.5em;
        margin-right: 0.5em;
    }
</style>

<script>
    import _ from 'lodash';


    export default {
        name: 'ExportForm',
        props: {
            maxExportCount: {
                type: Number,
                default: 1000,
            },
        },
        data() {
            return {
                exportMode: 'all',
                exportCount: 1000,
                orderColumn: 'last_visit_date',
                orderAscending: false,
                exportUsername: '',
                exportLabel: '',
                exportDescription: '',
            };
        },
        computed: {
            isSubsetSelected() {
                return this.exportMode === 'subset';
            },
        },
        methods: {
            getExportArgs() {
                const exportArgs = {
                    userid: this.exportUsername,
                    label: this.exportLabel,
                    description: this.exportDescription,
                };

                if (!this.isSubsetSelected) {
                    return exportArgs;
                }

                return _.defaults(exportArgs, {
                    limit: this.exportCount,
                    order_by: this.orderColumn,
                    order_asc: this.orderAscending,
                });
            },
        },
    };
</script>
