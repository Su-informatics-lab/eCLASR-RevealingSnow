<template>
    <div class="snow-file-loader">
        <div class="snow-file-drop-zone"
             :class="{isDragging: dragging}"
             @dragend="handleDragEnd"
             @dragleave="handleDragLeave"
             @dragover.prevent.stop="handleDragOver"
             @dragenter.prevent.stop="handleDragEnter"
             @drop.prevent.stop="handleDrop">
            Drop File Here
        </div>
    </div>
</template>

<style scoped>
    .snow-file-loader {

    }

    .snow-file-drop-zone {
        border: 2px dashed lightgrey;
        border-radius: 5px;
        padding: 25px;
        text-align: center;
        color: grey;
    }

    .isDragging {
        border: 2px dashed black;
        background: lightblue;
    }
</style>

<script>
    import _ from 'lodash';
    import Vue from 'vue';

    // Adapted from: https://www.html5rocks.com/en/tutorials/file/dndfiles/
    function readFileContents(file) {
        const reader = new FileReader();

        return new Promise((resolve, reject) => {
            reader.onload = () => {
                resolve(reader.result);
            };

            reader.onerror = () => {
                reject(reader.error);
            };

            reader.readAsArrayBuffer(file);
        });
    }

    export default {
        name: 'FileLoader',
        data() {
            return {
                dragging: false,
                files: {},
            };
        },
        methods: {
            handleDragOver(e) {
                this.dragging = true;
                e.dataTransfer.dropEffect = 'copy';
            },
            handleDragEnter() {
                this.dragging = true;
            },
            handleDragLeave() {
                this.dragging = false;
            },
            handleDragEnd() {
                this.dragging = false;
            },
            handleDrop(e) {
                this.dragging = false;
                if (!e.dataTransfer) {
                    return;
                }

                if (_.isEmpty(e.dataTransfer.files)) {
                    return;
                }

                this.handleFiles(e.dataTransfer.files);
            },
            handleFiles(files) {
                // If multiple files are uploaded, only handle the first one. Will
                // modify this behavior based on reported use case for multiple files
                // or expected behavior reported by users.
                this.uploadFile(_.first(files));
            },
            uploadFile(file) {
                readFileContents(file)
                    .then((contents) => {
                        this.addFile(file.name, contents);
                    })
                    .catch((err) => {
                        this.showErrorMessage(err);
                    });
            },
            showErrorMessage(msg) {
                this.$emit('file-error', msg);
            },
            addFile(filename, content) {
                Vue.set(this.files, filename, content);
                this.files[filename] = content;
                this.$emit('file-added', filename);
            },
            getFile(filename) {
                return this.files[filename];
            },
        },
    };
</script>
