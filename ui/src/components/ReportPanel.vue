<template>
    <div class="snow-report-panel">
        <div class="panel-label">
            <h5>{{ label }}</h5>
        </div>
        <slot/>
    </div>
</template>

<style scoped>
    .snow-report-panel {
        margin-top: 0.5em;
        padding-top: 0.5em;

        padding-bottom: 1em;
    }
</style>

<script>
    export default {
        name: 'ReportPanel',
        props: {
            label: {
                type: String,
                required: true,
            },
        },
    };
</script>
