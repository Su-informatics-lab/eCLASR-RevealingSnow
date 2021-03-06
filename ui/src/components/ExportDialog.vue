<template>
    <div class="snow-export-dialog">
        <sweet-modal ref="exportDialog"
                     title="Export Patients">
            <div class="snow-export-error alert alert-danger"
                 v-if="error !== null">
                Export Failed: {{ errorReason }}
            </div>

            <div class="snow-export-success alert alert-success"
                 v-if="exportComplete">
                Export Succeeded. You may close this window now.
            </div>

            <export-form ref="exportForm"
                         :max-export-count="maxExportCount"
            />

            <button slot="button"
                    type="button"
                    class="btn btn-secondary"
                    v-if="exportEnabled"
                    @click="startExport">
                Export to Tracking System
            </button>

            <button slot="button"
                    type="button"
                    class="btn btn-primary"
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

    .sweet-buttons > button {
        margin-left: 0.5em;
        margin-right: 0.5em;
    }
</style>

<style scoped>
    .snow-export-dialog {

    }

    .snow-export-error {
        padding: 1em;
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
        data() {
            return {
                error: null,
                errorReason: null,
                exportComplete: false,
            };
        },
        methods: {
            showDialog() {
                this.error = null;
                this.exportComplete = false;
                this.$refs.exportDialog.open();
            },
            closeDialog() {
                this.error = null;
                this.exportComplete = false;
                this.$refs.exportDialog.close();
            },
            startDownload() {
                const exportArgs = this.$refs.exportForm.getExportArgs();

                window.location.href = this.$api.getDownloadUrl(
                    this.$store.state.filters, exportArgs);
            },
            startExport() {
                const exportArgs = this.$refs.exportForm.getExportArgs();

                this.$api.exportToRemoteTrackingSystem(this.$store.state.filters, exportArgs)
                    .then(() => {
                        this.error = null;
                        this.exportComplete = true;
                    }, (error) => {
                        this.error = error;
                        this.errorReason = error.response.text;
                        this.exportComplete = false;
                });
            },
        },
        computed: {
            filterCriteriaIsSet() {
                return !_.isEmpty(this.$store.state.filters.criteria);
            },
            maxExportCount() {
                return this.$store.getters.patientCountFiltered;
            },
            exportEnabled() {
                return this.$store.getters.getFeature('TRACKING_API_ENABLED');
            },
        },
    };
</script>
