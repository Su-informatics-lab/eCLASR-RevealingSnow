<template>
    <div class="snow-export-dialog">
        <sweet-modal ref="exportDialog"
                     title="Export Patients">
            <export-form ref="exportForm"
                         :max-export-count="maxExportCount"
            />

            <button slot="button"
                    type="button"
                    class="btn btn-secondary"
                    @click="startDownload">
                Download
            </button>
        </sweet-modal>

        <div class="export-button"
             v-if="filterCriteriaIsSet">
            <button @click="showDialog"
                    id="export-filtered"
                    type="button"
                    class="btn btn-secondary">
                Export Patients
            </button>
        </div>

    </div>
</template>


<style>
    .sweet-title > h2 {
        line-height: inherit;
    }
</style>

<style scoped>
    .snow-export-dialog {

    }

    .export-button {
        position: fixed;
        top: 1em;
        right: 1em;
        z-index: 100;
    }
</style>

<script>
    import _ from 'lodash';
    import { SweetModal, SweetModalTab } from 'sweet-modal-vue';
    import ExportForm from './ExportForm';


    export default {
        name: 'ExportDialog',
        components: {
            SweetModal,
            SweetModalTab,
            ExportForm,
        },
        methods: {
            showDialog() {
                this.$refs.exportDialog.open();
            },
            startDownload() {
                const limit = this.$refs.exportForm.getLimitArgs();

                window.location.href = this.$api.getExportUrl(this.$store.state.filters, limit);
            },
        },
        computed: {
            filterCriteriaIsSet() {
                return !_.isEmpty(this.$store.state.filters.criteria);
            },
            maxExportCount() {
                return this.$store.getters.patientCountFiltered;
            },
        },
    };
</script>
