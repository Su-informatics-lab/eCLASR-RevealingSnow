<template>
    <div class="snow-metadata-uploader">
        <sweet-modal ref="uploadDialog"
                     title="Import Metadata">
            <vue-clip :options="vcopts">
                <template slot="clip-uploader-action">
                    <div>
                        <div class="dz-message">
                            Drop file here or click to upload.
                        </div>
                    </div>
                </template>

                <template slot="clip-uploader-body"
                          slot-scope="props">
                    <div v-for="(file, i) in props.files"
                         :key="file.id">
                        File {{ i }}: `{{ file }}`
                    </div>
                </template>
            </vue-clip>

            <!--
            <vue-transmit :options="uploadOptions"
                          url="/"
                          ref="uploader">
                Drop file here or click to upload.

                <template slot="files"
                          slot-scope="props">
                    <div v-for="(file, i) in props.files"
                         :key="file.id">
                        File {{ i }}: `{{ file }}`
                    </div>
                </template>
            </vue-transmit>
            -->
        </sweet-modal>
    </div>
</template>

<style scoped>
    .snow-metadata-uploader {

    }
</style>

<script>
    import 'vue-transmit/dist/vue-transmit.css';

    import { VueTransmit } from 'vue-transmit';
    import { SweetModal } from 'sweet-modal-vue';


    export default {
        name: 'MetadataUploader',
        components: {
            VueTransmit,
            SweetModal,
        },
        data() {
            return {
                uploadOptions: {
                    // TODO: Check on these
                    acceptedFileTypes: ['text/yaml', 'application/zip'],
                    adapterOptions: {
                        url: '/',
                        errUploadError: (xhr) => {
                            console.log(`Got an error: ${xhr}`);
                            return xhr.response.message;
                        },
                    },
                },
                vcopts: {},
                fileContent: '',
            };
        },
        methods: {
            showDialog() {
                this.error = null;
                this.$refs.uploadDialog.open();
            },
            closeDialog() {
                this.error = null;
                this.$refs.uploadDialog.close();
            },
        },
    };
</script>
