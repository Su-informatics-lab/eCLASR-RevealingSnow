<template>
    <div class="snow-dashboard row">
        <filter-panel class="col-12 col-xl-2 col-md-4"/>
        <report class="col-12 col-xl col-md-7"/>
    </div>
</template>

<style scoped>
    .snow-dashboard {
        text-align: left;
        margin: 0.5em;
        padding: 0.5em;
    }
</style>

<script>
    import FilterPanel from './FilterPanel';
    import Report from './Report';


    export default {
        name: 'Dashboard',
        components: {
            FilterPanel,
            Report,
        },
    };
</script>
