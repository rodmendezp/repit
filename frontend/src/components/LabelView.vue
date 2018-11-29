<template>
    <!--<td class="left-td"><label for="id_keep_labeling">Keep Labeling</label></td>-->
    <!--<td><input type="checkbox" :checked="keepLabeling" @input="keepLabelingCheckboxInput" id="id_keep_labeling"/></td>-->
    <div class="main-container full-height">
        <div class="content-container full-height" v-if="status === 'idle'">
            <twitch-player v-if="highlight"
                           :videoId="highlight.video_id"
                           :stTime="highlight.st_time"
                           :endTime="highlight.end_time"
            ></twitch-player>
            <label-type @type-setted="typeSetted = true" class="label-type-container"></label-type>
            <button :disabled="!typeSetted" class="btn btn-primary" @click="submitLabel">Submit</button>
        </div>
        <div v-else-if="status === 'processing'">
            <h1>LOADING</h1>
        </div>
        <div v-else-if="status === 'exception'">
            <h1>{{ exception }}</h1>
        </div>
    </div>
</template>

<script>
    import { mapGetters, mapActions, mapMutations } from 'vuex';
    import bDropdownItem from 'bootstrap-vue/es/components/dropdown/dropdown-item';
    import bDropdown from 'bootstrap-vue/es/components/dropdown/dropdown';
    import TwitchPlayer from './player/TwitchPlayer';
    import LabelType from './label/LabelType';

    export default {
        name: 'LabelView',
        components: {
            LabelType,
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
                exception: '',
                typeSetted: false,
            };
        },
        methods: {
            ...mapActions({
                getTypesDB: 'highlight/getTypesDB',
                postHighlight: 'highlight/postHighlight',
                requestPostJobAck: 'filler/requestPostJobAck',
                requestGetTask: 'filler/requestGetTask',
                requestSetVideoInfo: 'twitchdata/requestSetVideoInfo',
            }),
            ...mapMutations({
                setStatus: 'highlight/setStatus',
                setKeepLabeling: 'label/setKeepLabeling',
                setHighlight: 'highlight/setHighlight',
                setHighlightType: 'highlight/setHighlightType',
                setHighlightStart: 'highlight/setHighlightStart',
                setHighlightEnd: 'highlight/setHighlightEnd',
                setDeliveryTag: 'filler/setDeliveryTag',
            }),
            submitLabel() {
                this.setHighlightStart(this.videoStartTime);
                this.setHighlightEnd(this.videoEndTime);
                this.postHighlight(this.highlight);
                this.requestPostJobAck();
                this.setDeliveryTag(null);
                if (this.keepLabeling) {
                    const params = {
                        game: this.game,
                        streamer: this.streamer !== null ? this.streamer : '',
                        user: this.streamer !== null ? this.user : '',
                    };
                    this.setStatus('processing');
                    this.requestTaskLoop(params);
                }
                this.$router.push('/');
            },
            requestTaskLoop(params) {
                this.requestGetTask(params).then((response) => {
                    if (response.task !== undefined) {
                        this.setDeliveryTag(response.task.delivery_tag);
                        delete response.task.delivery_tag;
                        this.setHighlight(response.task);
                        this.requestSetVideoInfo(response.task.video_id);
                        this.$router.push('/label/');
                    } else if (response.exception !== undefined) {
                        this.setStatus('exception');
                        this.exception = response.exception;
                    } else if (response.message !== undefined && response.message !== 'Something went wrong') {
                        setTimeout(this.requestTaskLoop, 5000, params);
                    } else {
                        console.log('There was an error somewhere');
                    }
                });
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
    .main-container
        display: flex
        flex-direction: column
        justify-content: center
        align-items: center

    .content-container
        display: flex
        flex-direction: column
        justify-content: center
        align-items: center

    .label-type-container
        margin-top: 15px

    /*@media only screen and (min-width: 1024px)*/
        /*.content-container*/
            /*justify-content: center*/

    /*@media only screen and (orientation: landscape) and (max-width: 1023px)*/
        /*.content-container*/
            /*width: 100%*/
</style>
