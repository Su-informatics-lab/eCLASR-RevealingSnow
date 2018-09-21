<template>
    <div class="snow-export-dialog">
        <sweet-modal ref="export">
            Content.
        </sweet-modal>

        <div class="export-button"
             v-if="filterCriteriaIsSet">
            <a @click="showDialog"
               id="export-filtered"
               class="btn btn-secondary">
                Export Patients
            </a>
        </div>

    </div>
</template>

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


    export default {
        name: 'ExportDialog',
        components: {
            SweetModal,
            SweetModalTab,
        },
        methods: {
            showDialog() {
                this.$refs.export.open();
            },
        },
        computed: {
            filterCriteriaIsSet() {
                return !_.isEmpty(this.$store.state.filters.criteria);
            },
        },
    };
</script>
