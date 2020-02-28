<template>
    <div id="snow-footer">
        <div class="app-name">{{ applicationName }}</div>
        <div class="app-version">v{{ versionNumber }}</div>
    </div>
</template>

<style scoped>
    #snow-footer {
        border-top: 1px solid lightgrey;
        margin: 0 0 0.25em 0;
        padding: 0.5em;
        font-size: smaller;
    }

    #snow-footer .app-name {
        display: inline;
    }

    #snow-footer .app-version {
        display: inline;
    }
</style>

<script>
    import { mapGetters } from 'vuex';


    export default {
        name: 'Footer',
        computed: {
            ...mapGetters(['applicationVersion']),
            applicationName() {
                return this.applicationVersion.label;
            },
            versionNumber() {
                return this.applicationVersion.version;
            },
        },
    };
</script>
