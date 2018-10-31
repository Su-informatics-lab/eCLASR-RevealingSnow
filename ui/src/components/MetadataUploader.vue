<template>
    <div class="snow-metadata-uploader">
        <sweet-modal ref="uploadDialog"
                     title="Import Metadata">

            <div class="snow-import-error alert alert-danger"
                 v-if="error !== null">
                Export Failed: {{ errorReason }}
            </div>

            <file-loader ref="loader"
                         :accepted-file-types="['.zip', '.yml', '.yaml']"
                         @file-added="fileAdded"
                         @file-error="fileErr"/>
        </sweet-modal>
    </div>
</template>

<style scoped>
    .snow-metadata-uploader {

    }

    .snow-import-error {
        padding: 1em;
    }
</style>

<script>
    import { SweetModal } from 'sweet-modal-vue';
    import yaml from 'js-yaml';
    import { createFiltersFromMetadata } from '@/util';
    import { mapGetters } from 'vuex';

    import FileLoader from './FileLoader';


    function loadMetadataContent(content) {
        const contentAsString = String.fromCharCode.apply(null, new Uint8Array(content));
        return yaml.safeLoad(contentAsString);
    }

    function extractMetadataFromZip() {
        // TODO
        throw new Error('ZIP files not yet supported');
    }

    function getMetadataFromFile(filename, content) {
        return new Promise((resolve, reject) => {
            const lowerFile = filename.toLowerCase();
            if (lowerFile.endsWith('.yml')) {
                resolve(loadMetadataContent(content));
            } else if (lowerFile.endsWith('.zip')) {
                resolve(extractMetadataFromZip(content));
            } else {
                reject(new Error(`Unexpected file type ${filename}`));
            }
        });
    }

    export default {
        name: 'MetadataUploader',
        components: {
            FileLoader,
            SweetModal,
        },
        data() {
            return {
                error: null,
                errorReason: null,
                file: null,
            };
        },
        methods: {
            showDialog() {
                this.clearError();
                this.$refs.uploadDialog.open();
            },
            closeDialog() {
                this.clearError();
                this.$refs.uploadDialog.close();
            },
            fileAdded(filename) {
                this.clearError();
                const fileContent = this.$refs.loader.getFile(filename);

                getMetadataFromFile(filename, fileContent)
                    .then(metadata => createFiltersFromMetadata(this.model, metadata))
                    .then((filters) => {
                        this.$emit('metadata-uploaded', filters);
                    })
                    .then(() => {
                        this.closeDialog();
                    })
                    .catch((err) => {
                        this.setError(err);
                    });
            },
            fileErr(err) {
                this.setError(err);
            },
            setError(err) {
                this.error = err;
                this.errorReason = err.message;
            },
            clearError() {
                this.error = null;
                this.errorReason = null;
            },
        },
        computed: {
            ...mapGetters(['model']),
        },
    };
</script>
