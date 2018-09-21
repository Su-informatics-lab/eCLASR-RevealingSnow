<template>
    <div class="snow-ternary-toggle"
         :data-enabled="enabled"
         @click="nextState">
        <font-awesome-icon class="icon-button"
                           :icon="icon"/>
    </div>
</template>

<style scoped>
    .snow-ternary-toggle {
        display: inline;
    }

    .snow-ternary-toggle[data-enabled="true"] {
        cursor: pointer;
    }

    .snow-ternary-toggle:not([data-enabled="true"]) {
        cursor: not-allowed;
    }

    svg[data-icon="times-circle"] {
        color: red;
    }

    svg[data-icon="plus-circle"] {
        color: green;
    }
</style>

<script>
    import FontAwesomeIcon from '@fortawesome/vue-fontawesome';
    import { faCircleNotch, faPlusCircle, faTimesCircle } from '@fortawesome/fontawesome-free-solid';


    const icons = {
        null: faCircleNotch,
        true: faPlusCircle,
        false: faTimesCircle,
    };

    export default {
        name: 'TernaryToggle',
        props: {
            value: {
                type: Boolean,
                default: null,
            },
            enabled: {
                type: Boolean,
                default: true,
            },
        },
        data() {
            return {
                state: this.value,
            };
        },
        components: {
            FontAwesomeIcon,
        },
        computed: {
            icon() {
                return icons[this.state];
            },
        },
        methods: {
            nextState() {
                if (!this.enabled) {
                    return;
                }

                let nextState;

                switch (this.state) {
                case null:
                    nextState = true;
                    break;

                case true:
                    nextState = false;
                    break;

                default:
                case false:
                    nextState = null;
                    break;
                }

                this.setState(nextState);
            },
            setState(newState) {
                this.state = newState;
            },
        },
        watch: {
            value(newValue) {
                this.setState(newValue);
            },
            state(newValue) {
                this.$emit('input', newValue);
            },
        },
    };
</script>
