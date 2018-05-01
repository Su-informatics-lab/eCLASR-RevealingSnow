<template>
    <div class="rs-barchart"/>
</template>

<style>
</style>

<script>
    import BarChart from 'britecharts/dist/umd/bar.min';
    import tooltip from 'britecharts/dist/umd/miniTooltip.min';

    import 'britecharts/dist/css/britecharts.min.css';

    import * as d3Selection from 'd3-selection';


    export default {
        data() {
            return {
                container: null,
                chart: null,
                tooltip: null,
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
                        left: 100,
                        right: 20,
                        top: 20,
                        bottom: 30,
                    };
                },
            },
            numberFormat: {
                type: String,
                default: ',d',
            },
        },
        watch: {
            data(value) {
                this.container.datum(value).call(this.chart);

                if (!this.tooltip) {
                    this.createTooltip();
                }
            },
        },
        mounted() {
            this.container = d3Selection.select(this.$el);
            this.chart = new BarChart();

            this.chart
                .isAnimated(true)
                .width(this.width)
                .height(this.height)
                .margin(this.margin)
                .numberFormat(this.numberFormat)
                .yAxisPaddingBetweenChart(10)
            ;
        },
        methods: {
            createTooltip() {
                this.tooltip = tooltip();
                this.tooltip
                    .numberFormat(this.numberFormat);

                const tooltipContainer = this.container.select('.bar-chart .metadata-group');
                tooltipContainer.datum([]).call(this.tooltip);

                this.chart
                    .on('customMouseOver', this.tooltip.show)
                    .on('customMouseMove', this.tooltip.update)
                    .on('customMouseOut', this.tooltip.hide);
            },
        },
    };
</script>
