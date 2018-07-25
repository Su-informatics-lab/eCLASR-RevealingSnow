<template>
    <div id="app"
         class="container-fluid">
        <masthead/>
        <dashboard/>
    </div>
</template>

<style scoped>
    #app {
        font-family: 'Avenir', Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-align: center;
        color: #2c3e50;
        margin-top: 1em;
    }
</style>

<script>
    import Dashboard from './components/Dashboard';
    import Masthead from './Masthead';


    export default {
        name: 'App',
        components: {
            Dashboard,
            Masthead,
        },
        mounted() {
            this.$store.dispatch('loadUnfilteredStats');
        },
    };
</script>
