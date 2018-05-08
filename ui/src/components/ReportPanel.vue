<template>
    <div class="snow-report-panel">
        <div class="panel-label">{{ label }}</div>
        <slot/>
    </div>
</template>

<style scoped>

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
