<template>
    <div class="snow-dashboard row">
        <filters class="col-12 col-xl-2 col-md-4"/>
        <report class="col-12 col-xl col-md-7"/>
    </div>
</template>

<style scoped>
    .snow-dashboard {
        text-align: left;
        margin: 0;
        padding: 0;
    }
</style>

<script>
    import Filters from './Filters';
    import Report from './Report';


    export default {
        name: 'Dashboard',
        components: {
            Filters,
            Report,
        },
    };
</script>
