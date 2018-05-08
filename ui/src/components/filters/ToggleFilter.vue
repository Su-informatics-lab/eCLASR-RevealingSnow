<template>
    <div class="snow-toggle-filter form-check">
        <label class="form-check-label">
            <input type="checkbox"
                   class="form-check-input"
                   v-model="value">
            {{ label }}
        </label>
    </div>
</template>

<style scoped>

</style>

<script>
    export default {
        name: 'ToggleFilter',
        props: {
            label: {
                type: String,
                required: true,
            },
        },
        data() {
            return {
                value: null,
            };
        },
    };
</script>
