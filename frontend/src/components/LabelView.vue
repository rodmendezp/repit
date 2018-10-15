<template>
    <div class="row full-height align-items-center">
        <div class="col"></div>
        <div class="col" v-if="status === 'idle'">
            <twitch-player v-if="highlight"
                :videoId="highlight.video_id"
                :stTime="highlight.st_time"
                :endTime="highlight.end_time"
            ></twitch-player>
            <div class="label-form">
                <table class="table-form">
                    <tr class="height-tr">
                        <td class="left-td"><label for="id_description">Description</label></td>
                        <td class="left-td"><input v-model="label.description" id="id_description"/></td>
                    </tr>
                    <tr class="height-tr">
                        <td class="left-td"><label>Type</label></td>
                        <td>
                            <b-dropdown variant="primary" class="btn-primary type-dropdown" :text="label.type">
                                <b-dropdown-item class="type-dropdown-item" v-for="labelType in types" :key="labelType"
                                                 :value="labelType" @click="setType(labelType)">
                                    {{ labelType }}
                                </b-dropdown-item>
                            </b-dropdown>
                        </td>
                    </tr>
                    <tr class="height-tr">
                        <td class="left-td"><label for="id_keep_labeling">Keep Labeling</label></td>
                        <td><input type="checkbox" :checked="keepLabeling" @input="keepLabelingCheckboxInput" id="id_keep_labeling"/></td>
                    </tr>
                </table>
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
                requestPostJobAck: 'filler/requestPostJobAck',
            }),
            ...mapMutations({
                setStatus: 'highlight/setStatus',
                setKeepLabeling: 'label/setKeepLabeling',
                setHighlightType: 'highlight/setHighlightType',
                setHighlightStart: 'highlight/setHighlightStart',
                setHighlightEnd: 'highlight/setHighlightEnd',
                setDeliveryTag: 'filler/setDeliveryTag',
            }),
            submitLabel() {
                if (this.label.type === 'Choose Type') return;
                this.setHighlightStart(this.videoStartTime);
                this.setHighlightEnd(this.videoEndTime);
                this.postHighlight(this.highlight);
                this.requestPostJobAck();
                this.setDeliveryTag(null);
                if (this.keepLabeling) {
                    this.setStatus('processing');
                    this.webSocket.send(JSON.stringify({
                        message: 'GET_HIGHLIGHT',
                        params: {
                            game: this.game,
                            streamer: this.streamer !== null ? this.streamer : '',
                            user: this.streamer !== null ? this.user : '',
                        },
                    }));
                }
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
                game: 'label/getGame',
                streamer: 'label/getStreamer',
                user: 'label/getUser',
                videoStartTime: 'player/getVideoStartTime',
                videoEndTime: 'player/getVideoEndTime',
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
        margin-top: 90px
        text-align: center

    .table-form
        margin: 0 auto 20px

    .left-td
        text-align: left

    .height-tr
        height: 40px

    label
        color: white
        margin-bottom: 0

    .type-dropdown
        background-color: transparent

    .form-block
        margin-top: 5px
        margin-bottom: 5px

    .form-block label
        display: inline-block
        width: 100px
        text-align: right
        color: white
</style>
