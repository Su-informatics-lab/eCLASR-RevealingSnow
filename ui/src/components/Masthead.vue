<template>
    <div id="snow-masthead">
        <img id="us-pointer-logo"
             src="../assets/logo.png">
        <version-header />
    </div>
</template>

<style scoped>
    #us-pointer-logo {
    }

    #snow-masthead {
        margin-top: 1em;
        margin-bottom: 1em;
    }
</style>

<script>
    import VersionHeader from './VersionHeader';

    export default {
        name: 'Masthead',
        components: {
            VersionHeader,
        },
    };
</script>
