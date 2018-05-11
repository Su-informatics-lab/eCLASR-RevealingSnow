<template>
    <div class="snow-mode-switch row justify-content-center">
        <div class="btn-group btn-group-toggle"
             data-toggle="buttons">
            <label class="btn  btn-light active">
                <input type="radio"
                       name="mode"
                       id="mode-filtered">
                Filtered
            </label>

            <label class="btn btn-light">
                <input type="radio"
                       name="mode"
                       id="mode-total">
                Total
            </label>
        </div>
    </div>
</template>

<style scoped>
    .snow-mode-switch {
        padding-bottom: 1em;
        margin-bottom: 1em;
        border-bottom: 1px solid lightgrey;
    }
</style>

<script>
    export default {
        name: 'ModeSwitch',
        data() {
            return {
                mode: 0,
            };
        },
    };
</script>
