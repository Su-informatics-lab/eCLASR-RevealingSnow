<template>
    <div class="snow-barchart">
        <div ref="chart-container"/>

        <div class="chart-size-toggler"
             v-if="allowResize"
             @click="toggleSizeMode">
            <font-awesome-icon :icon="toggleIcon"/>
        </div>
    </div>
</template>

<style>
    .snow-barchart {
        display: inline-block;
        position: relative;
    }

    .chart-size-toggler {
        position: absolute;
        top: 0;
        right: 0;

        cursor: pointer;
    }
</style>

<script>
    import FontAwesomeIcon from '@fortawesome/vue-fontawesome';
    import { faCompress, faExpand } from '@fortawesome/fontawesome-free-solid';

    import * as bb from 'billboard.js';
    import 'billboard.js/dist/billboard.min.css';
    import _ from 'lodash';


    function getAllXValues(data) {
        if (!data) {
            return [];
        }

        // Get the list of x-values present across all categories
        return _.uniq(_.flatMap(_.mapValues(data, x => _.map(x, 'name'))));
    }

    function alignData(data) {
        const keys = getAllXValues(data);

        // Rebuild the dataset, ensuring that each category has the same set of 'x' values.
        return _.mapValues(data, (category) => {
            const valueLookup = _.keyBy(category, 'name');

            return _.map(keys, (d) => {
                const v = _.get(valueLookup, d, null);

                return {
                    name: d,
                    value: v !== null ? v.value : null,
                };
            });
        });
    }

    function transformData(data, orderFn, transformFn) {
        return _.mapValues(data, (d) => {
            const sorted = orderFn(d);
            return transformFn(sorted);
        });
    }

    function combineDataCategories(data) {
        const dataValues = _.mapValues(data, x => _.map(x, 'value'));
        const pairedKeyValues = _.toPairs(dataValues);

        return _.map(pairedKeyValues, _.flatten);
    }

    function getMissingKeys(oldData, newData) {
        if (!oldData) {
            return [];
        }

        const oldKeys = _.keys(oldData);
        const newKeys = _.keys(newData);

        return _.difference(oldKeys, newKeys);
    }

    export default {
        data() {
            return {
                chart: null,
                expanded: false,
                alignedData: null,
                transformedData: null,
            };
        },
        props: {
            data: { type: Object, required: true },
            width: { type: Number, required: true },
            height: { type: Number, required: true },
            title: { type: String, default: '' },
            maxWidth: { type: Number, default: 0 },
            maxHeight: { type: Number, default: 0 },
            allowResize: { type: Boolean, default: false },
            options: {
                type: Object,
                default() {
                    return {};
                },
            },
            orderFunction: {
                type: Function,
                default: data => _.sortBy(data, d => d.name),
            },
            transformFunction: {
                type: Function,
                default: data => data,
            },
            dataLegend: {
                type: Object,
                default() {
                    return {};
                },
            },
            groupLegend: {
                type: Object,
                default() {
                    return {};
                },
            },
            groupColors: {
                type: Object,
                default() {
                    return {};
                },
            },
            xAxisLabel: {
                type: String,
                default: '',
            },
            yAxisLabel: {
                type: String,
                default: '',
            },
            percentByGroup: {
                type: Boolean,
                default: true,
            },
        },
        watch: {
            data(value) {
                this.setData(value);
            },
            width(value) {
                this.chart.config('size_width', value, true);
            },
            height(value) {
                this.chart.config('size_height', value, true);
            },
        },
        mounted() {
            const baseConfig = {
                bindto: this.$refs['chart-container'],
                data: {
                    x: 'x',
                    columns: [],
                    type: 'bar',
                },
            };


            const chartConfig = _.defaultsDeep(baseConfig, this.options, {
                size: {
                    width: this.width,
                    height: this.height,
                },
                axis: {
                    x: {
                        type: 'category',
                    },
                },
                legend: {
                    show: false,
                },
                tooltip: {
                    format: {
                        title: this.getTooltipTitle,
                        value: this.getTooltipValue,
                    },
                },
            });

            if (this.xAxisLabel) {
                chartConfig.axis.x.label = {
                    text: this.xAxisLabel,
                    position: 'outer-right',
                };
            }

            if (this.yAxisLabel) {
                chartConfig.axis.y = {
                    label: {
                        text: this.yAxisLabel,
                        position: 'outer-top',
                    },
                };
            }

            if (this.title) {
                chartConfig.title = {
                    text: this.title,
                    position: 'top-center',
                };
            }

            this.chart = bb.bb.generate(chartConfig);

            if (this.data) {
                this.setData(this.data);
            }
        },
        methods: {
            setData(value) {
                const aligned = alignData(value);

                // Identify any data groups that should be removed
                const missingKeys = getMissingKeys(this.alignedData, aligned);

                this.alignedData = aligned;
                this.transformedData = transformData(
                    this.alignedData,
                    this.orderFunction, this.transformFunction,
                );

                const keys = getAllXValues(this.transformedData);
                const combined = combineDataCategories(this.transformedData);

                this.setAllData(keys, combined, missingKeys);

                if (this.groupLegend) {
                    this.chart.data.names(this.groupLegend);
                }

                if (this.groupColors) {
                    this.chart.data.colors(this.groupColors);
                }
            },
            setAllData(keys, combined, missing) {
                const dataToLoad = [
                    _.flatten([['x'], keys]),
                    ...combined,
                ];

                this.chart.load({
                    columns: dataToLoad,
                    unload: missing,
                    categories: keys,
                });
            },
            getTooltipTitle(index) {
                const key = this.chart.categories()[index];

                if (!_.isEmpty(this.dataLegend)) {
                    return this.dataLegend[key].label;
                }

                return key;
            },
            getTooltipValue(name, ratio, id, index) {
                const groupTotalFn = this.groupTotalFunction;
                const groupTotal = groupTotalFn(id, index);
                const percentage = _.round(100.0 * (name / groupTotal), 2);

                return `${name} (${percentage}%)`;
            },
            totalByGroup(id) {
                return _.sumBy(this.transformedData[id], 'value');
            },
            totalByIndex(id, index) {
                return _.sumBy(_.map(this.transformedData, d => d[index]), 'value');
            },
            toggleSizeMode() {
                this.expanded = !this.expanded;

                this.resizeChart({
                    width: this.expanded ? this.maxWidth : this.width,
                    height: this.expanded ? this.maxHeight : this.height,
                });
            },
            resizeChart({ width, height }) {
                // Using the chart.config method instead of resize because the latter doesn't
                // animate the change.
                this.chart.config('size_width', width, true);
                this.chart.config('size_height', height, true);

                this.$emit('resized');
            },
        },
        computed: {
            toggleIcon() {
                return this.expanded ? faCompress : faExpand;
            },
            groupTotalFunction() {
                return this.percentByGroup ? this.totalByGroup : this.totalByIndex;
            },
        },
        components: {
            FontAwesomeIcon,
        },
    };
</script>
