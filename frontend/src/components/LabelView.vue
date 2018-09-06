<template>
    <div class="row full-height align-items-center">
        <div class="col"></div>
        <div class="col">
            <twitch-player
                :videoId="$route.params.video_id"
                :stTime="$route.params.st_time"
                :endTime="$route.params.end_time"></twitch-player>
            <div class="label-form">
                <div class="form-block">
                    <label>Description</label>
                    <input v-model="label.description"/>
                </div>
                <div class="form-block">
                    <label>Type</label>
                    <b-dropdown class="btn-primary" :text="label.type">
                        <b-dropdown-item v-for="labelType in types"
                                         :key="labelType" :value="labelType" @click="console.log(types)">
                            {{ labelType }}
                        </b-dropdown-item>
                    </b-dropdown>
                </div>
                <div>
                    <label>Keep Labeling?</label>
                    <input type="checkbox"/>
                </div>
                <button class="btn btn-primary" @click="submitLabel">Submit</button>
            </div>
        </div>
        <div class="col"></div>
    </div>
</template>

<script>
    import { mapGetters, mapActions } from 'vuex';
    import bDropdownItem from 'bootstrap-vue/es/components/dropdown/dropdown-item';
    import bDropdown from 'bootstrap-vue/es/components/dropdown/dropdown';
    import TwitchPlayer from './player/TwitchPlayer';

    export default {
        name: 'LabelView',
        components: {
            TwitchPlayer,
            bDropdown,
            bDropdownItem,
        },
        data() {
            return {
                label: {
                    description: '',
                    type: 'Choose Type',
                },
                labelTypes: [],
                highlight: {
                    id: null,
                    start: null,
                    end: null,
                    description: null,
                    type: null,
                    video: null,
                },
            };
        },
        methods: {
            ...mapActions({
                getTypesDB: 'highlight/getTypesDB',
                putHighlight: 'highlight/putHighlight',
            }),
            fillHighlight() {
                this.highlight.id = this.highlight.id || this.$route.params.id;
                this.highlight.start = this.highlight.start || this.$route.params.st_time;
                this.highlight.end = this.highlight.end || this.$route.params.end_time;
                this.highlight.description = this.label.description;
                this.highlight.type = this.label.type;
            },
            submitLabel() {
                this.fillHighlight();
                if (this.label.type === 'Choose Type') {
                    return;
                }
                this.putHighlight(this.highlight);
            },
        },
        computed: {
            ...mapGetters({
                types: 'highlight/getTypes',
            }),
        },
        mounted() {
            if (this.types === null) this.getTypesDB();
        },
    };
</script>

<style lang="sass">
    .label-form
        text-align: center
</style>
