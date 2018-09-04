<template>
    <div class="snow-chart-demographic-histogram">
        <histogram :data="demographicData"
                   :width="width"
                   :height="height"
                   :cumulative="cumulative"
                   :group-legend="demographicLegend"
                   :chart-options="{bar: {width: {ratio: 0.9}}, legend: true}"
                   :allow-resize="allowResize"
                   :title="transformedTitle"
                   @resized="$emit('resized')"
        />
    </div>
</template>

<style scoped>

</style>

<script>
    import _ from 'lodash';

    import Histogram from './Histogram';


    export default {
        name: 'DemographicHistogram',
        props: {
            data: { type: Object, required: true },
            demographic: { type: String, required: true },
            width: { type: Number, required: true },
            height: { type: Number, required: true },
            allowResize: { type: Boolean, default: false },
            title: { type: String, default: '' },
            cumulative: {
                type: Boolean,
                default: false,
            },
            groupLegend: {
                type: Object,
                default() {
                    return {};
                },
            },
        },
        components: {
            Histogram,
        },
        computed: {
            demographicData() {
                return this.data[this.demographic] || {};
            },
            demographicLegend() {
                const legend = _.keyBy(this.$store.getters.getLegendObject(this.demographic), 'key');
                return _.mapValues(legend, 'label');
            },
            transformedTitle() {
                return _.startCase(this.title);
            },
        },
        methods: {
            makeBigger() {
                this.width = this.width * 2;
            },
        },
    };
</script>
