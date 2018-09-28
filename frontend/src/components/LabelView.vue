<template>
    <div class="row full-height align-items-center">
        <div class="col"></div>
        <div class="col">
            <twitch-player v-if="highlight"
                :videoId="highlight.video_id"
                :stTime="highlight.st_time"
                :endTime="highlight.end_time"></twitch-player>
            <div class="label-form">
                <div class="form-block">
                    <label>Description</label>
                    <input v-model="label.description"/>
                </div>
                <div class="form-block">
                    <label>Type</label>
                    <b-dropdown class="btn-primary" :text="label.type">
                        <b-dropdown-item v-for="labelType in types"
                                         :key="labelType" :value="labelType" @click="label.type = labelType">
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
    import { mapGetters, mapActions, mapMutations } from 'vuex';
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
            };
        },
        methods: {
            ...mapActions({
                getTypesDB: 'highlight/getTypesDB',
                putHighlight: 'highlight/putHighlight',
            }),
            ...mapMutations({
                setStatus: 'highlight/setStatus',
            }),
            submitLabel() {
                if (this.label.type === 'Choose Type') {
                    return;
                }
                this.putHighlight(this.highlight);
            },
        },
        computed: {
            ...mapGetters({
                types: 'highlight/getTypes',
                highlight: 'highlight/getHighlight',
                webSocket: 'getWebSocket',
            }),
        },
        mounted() {
            if (this.types === null) this.getTypesDB();
            this.setStatus('idle');
        },
    };
</script>

<style lang="sass">
    .label-form
        text-align: center
</style>
