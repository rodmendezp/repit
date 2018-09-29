<template>
    <div class="row full-height align-items-center">
        <div class="col"></div>
        <div class="col" v-if="status === 'idle'">
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
                    <b-dropdown variant="primary" class="btn-primary type-dropdown" :text="label.type">
                        <b-dropdown-item v-for="labelType in types"
                                         :key="labelType" :value="labelType" @click="setType(labelType)">
                            {{ labelType }}
                        </b-dropdown-item>
                    </b-dropdown>
                </div>
                <div>
                    <label>Keep Labeling?</label>
                    <input type="checkbox" :checked="keepLabeling" @input="keepLabelingCheckboxInput"/>
                </div>
                <button class="btn btn-primary" @click="submitLabel">Submit</button>
            </div>
        </div>
        <div style="text-align: center" class="col" v-else-if="status === 'processing'">
            <div> LOADING </div>
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
                postHighlight: 'highlight/postHighlight',
            }),
            ...mapMutations({
                setStatus: 'highlight/setStatus',
                setKeepLabeling: 'label/setKeepLabeling',
                setHighlightType: 'highlight/setHighlightType',
            }),
            submitLabel() {
                if (this.label.type === 'Choose Type') return;
                this.postHighlight(this.highlight);
                this.setStatus('processing');
                this.webSocket.send(JSON.stringify({
                    message: 'GET_HIGHLIGHT',
                }));
                this.$router.push('/');
            },
            keepLabelingCheckboxInput() {
                this.setKeepLabeling(!this.keepLabeling);
            },
            setType(labelType) {
                this.setHighlightType(labelType);
                this.label.type = labelType;
            },
        },
        computed: {
            ...mapGetters({
                webSocket: 'getWebSocket',
                types: 'highlight/getTypes',
                status: 'highlight/getStatus',
                highlight: 'highlight/getHighlight',
                keepLabeling: 'label/getKeepLabeling',
            }),
        },
        mounted() {
            if (this.types === null) this.getTypesDB();
            this.setStatus('idle');
        },
    };
</script>

<style scoped lang="sass">
    .label-form
        text-align: center

    .label-form label
        display: inline-block
        width: 150px
        text-align: right
        color: white

    .label-form input
        margin-left: 10px
        border: 2px solid transparent

    .type-dropdown
        background-color: transparent
</style>
