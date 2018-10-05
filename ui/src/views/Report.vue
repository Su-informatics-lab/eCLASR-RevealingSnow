<template>
    <div class="snow-report">
        <export-dialog/>

        <report-panel label="Patient Totals"
                      class="totals">

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
                       title="Race"
                       :width="300"
                       :height="200"/>

            <dem-chart stats-key="sex"
                       title="Sex"
                       :width="300"
                       :height="200"/>

            <dem-chart stats-key="ethnicity"
                       title="Ethnicity"
                       :width="300"
                       :height="200"/>

            <histogram :data="ageData"
                       title="Age"
                       :width="900"
                       :height="200"
                       :group-legend="{filtered: 'Filtered', unfiltered: 'Unfiltered'}"/>
        </report-panel>

        <report-panel label="Conditions"
                      class="conditions">
            Placeholder
        </report-panel>

        <report-panel label="Cumulative YMCA Proximity"
                      id="ymca-proximity-panel"
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

    #ymca-proximity-panel {
        border-top: 1px solid lightgray;
        padding-top: 1em;
    }
</style>

<script>
    import { mapGetters } from 'vuex';

    import ReportPanel from '../components/ReportPanel';
    import DemChart from '../components/charts/GlobalDemographicChart';
    import Histogram from '../components/charts/Histogram';
    import YmcaSite from '../components/charts/YmcaSite';
    import ExportDialog from '../components/ExportDialog';


    export default {
        name: 'Report',
        components: {
            ReportPanel,
            DemChart,
            Histogram,
            YmcaSite,
            ExportDialog,
        },
        computed: {
            ...mapGetters(['enabledYmcaSites', 'patientCountUnfiltered', 'patientCountFiltered']),
            ageData() {
                return {
                    unfiltered: this.$store.state.stats.unfiltered.age || [],
                    filtered: this.$store.state.stats.filtered.age || [],
                };
            },
            exportUrl() {
                return this.$api.getDownloadUrl(this.$store.state.filters);
            },
        },
    };
</script>
