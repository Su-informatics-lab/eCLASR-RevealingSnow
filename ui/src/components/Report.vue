<template>
    <div class="snow-report">
        <report-panel label="Patient Totals"
                      class="totals">
            <div class="export-button"
                 v-if="filterCriteriaIsSet">
                <a :href="exportUrl"
                   id="export-filtered"
                   class="btn btn-secondary">
                    Export Patients
                </a>
            </div>

            <div class="patient-field">
                <span class="label">Unfiltered:</span>

                <span class="value">
                    {{ patientCountUnfiltered }}
                </span>
            </div>

            <div class="patient-field">
                <span class="label">Filtered:</span>

                <span class="value">
                    {{ patientCountFiltered }}
                </span>
            </div>
        </report-panel>

        <report-panel label="Demographics"
                      class="demographics">
            <dem-chart stats-key="race"
                       :width="300"
                       :height="200"/>

            <dem-chart stats-key="sex"
                       :width="300"
                       :height="200"/>

            <dem-chart stats-key="ethnicity"
                       :width="300"
                       :height="200"/>

            <histogram :unfiltered="ageUnfiltered"
                       :filtered="ageFiltered"
                       :width="900"
                       :height="200"/>
        </report-panel>

        <report-panel label="Conditions"
                      class="conditions">
            Placeholder
        </report-panel>

        <report-panel label="Cumulative YMCA Proximity"
                      class="ymca">
            <ymca-site v-for="site in enabledYmcaSites"
                       :key="site.site"
                       :id="site.site"
                       :width="450"
                       :height="200"/>
        </report-panel>
    </div>
</template>

<style scoped>
    .conditions {
        display: none;
    }

    .patient-field {
        padding-left: 1em;
    }

    .patient-field .label {
        font-weight: bold;
    }

    .export-button {
        float: right;
    }
</style>

<script>
    import _ from 'lodash';

    import { mapGetters } from 'vuex';

    import ReportPanel from './ReportPanel';
    import DemChart from './charts/GlobalDemographicChart';
    import Histogram from './charts/Histogram';
    import YmcaSite from './charts/YmcaSite';


    export default {
        name: 'Report',
        components: {
            ReportPanel,
            DemChart,
            Histogram,
            YmcaSite,
        },
        computed: {
            ...mapGetters(['enabledYmcaSites', 'patientCountUnfiltered', 'patientCountFiltered']),
            ageUnfiltered() {
                return this.$store.state.stats.unfiltered.age || [];
            },
            ageFiltered() {
                return this.$store.state.stats.filtered.age || [];
            },
            filterCriteriaIsSet() {
                return !_.isEmpty(this.$store.state.filters.criteria);
            },
            exportUrl() {
                return this.$api.getExportUrl(this.$store.state.filters.criteria);
            },
        },
        mounted() {
            this.$store.dispatch('getFilteredStats');
        },
    };
</script>
