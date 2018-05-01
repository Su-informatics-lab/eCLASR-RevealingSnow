<template>
    <div class="rs-barchart"/>
</template>

<style>
</style>

<script>
    import BarChart from 'britecharts/dist/umd/bar.min';
    import * as d3Selection from 'd3-selection';


    export default {
        data() {
            return {
                container: null,
                chart: null,
            };
        },
        props: {
            data: { type: Array, required: true },
            width: { type: String, required: true },
            height: { type: String, required: true },
            margin: {
                type: Object,
                default() {
                    return {
                        left: 50,
                        right: 20,
                        top: 20,
                        bottom: 30,
                    };
                },
            },
        },
        watch: {
            data(value) {
                this.container.datum(value).call(this.chart);
            },
        },
        mounted() {
            this.container = d3Selection.select(this.$el);
            this.chart = new BarChart();
            this.chart
                .isAnimated(true)
                .width(this.width)
                .height(this.height)
                .margin(this.margin);
        },
    };
</script>
