<template>
    <div id="snow-data-version-summary">
        <div class="snow-version"
             v-for="v in versionDetails"
             :key="v.key"
             :id="v.key">
            <span class="snow-version-label">{{ v.label }}:</span>
            <span class="snow-version-date">{{ v.date }}</span>
        </div>
    </div>
</template>

<style scoped>
    #snow-data-version-summary {
        position: absolute;
        top: 1em;
        left: 1em;
        z-index: 100;
        text-align: left;
        font-size: smaller;
    }

    .snow-version-label {
        font-weight: bold;
    }

    .snow-version-date {

    }
</style>

<script>
    import { mapGetters } from 'vuex';


    const VERSION_KEYS_TO_DISPLAY = ['emr_pull', 'exported_column'];

    export default {
        name: 'VersionHeader',
        computed: {
            ...mapGetters(['getVersionKeys']),
            versionDetails() {
                return this.getVersionKeys(VERSION_KEYS_TO_DISPLAY);
            },
        },
    };
</script>
