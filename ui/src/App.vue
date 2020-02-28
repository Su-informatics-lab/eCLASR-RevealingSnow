<template>
    <div id="app"
         class="container-fluid">
        <masthead/>
        <dashboard/>
        <app-footer/>
    </div>
</template>

<style scoped>
    #app {
        font-family: 'Avenir', Helvetica, Arial, sans-serif;
        font-size: small;

        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-align: center;
        color: #2c3e50;

        padding: 0;
    }
</style>

<script>
    import Dashboard from './views/Dashboard';
    import Masthead from './components/Masthead';
    import AppFooter from './components/AppFooter';


    export default {
        name: 'App',
        components: {
            Dashboard,
            Masthead,
            AppFooter,
        },
        mounted() {
            this.$store.dispatch('getFeatureFlags');
            this.$store.dispatch('loadUnfilteredStats');
        },
    };
</script>
