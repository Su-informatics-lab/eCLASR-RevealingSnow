<template>
    <div class="snow-distance-filter">
        <label>
            Distance to YMCA Fulton:
            <select class="distances form-control"
                    v-model="distance">
                <option value="-1">Any Distance</option>
                <option value="1">1 Mile</option>
                <option value="5">5 Miles</option>
                <option value="15">15 Miles</option>
            </select>
        </label>
    </div>
</template>

<style scoped>

</style>

<script>
    export default {
        name: 'DistanceFilter',
        props: {
            id: {
                type: String,
                required: true,
            },
            label: {
                type: String,
                required: true,
            },
        },
        data() {
            return {
                distance: '5',
            };
        },
        computed: {
            value() {
                if (this.distance === '-1') {
                    return null;
                }

                return this.distance;
            },
        },
    };
</script>
