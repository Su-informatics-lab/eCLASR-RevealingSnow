<template>
    <div class="snow-dashboard">
        <filter-panel/>
        <report/>
    </div>
</template>

<style scoped>

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
