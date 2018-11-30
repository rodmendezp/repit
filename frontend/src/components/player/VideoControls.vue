<template>
    <div>
        <table class="video-controls-table">
            <tr>
                <td class="play">
                    <button class="btn-fa-style" :disabled="!ready" :size="'sm'" @click="playPause">
                        <template v-if="playing"><i class="fa fa-pause"></i></template>
                        <template v-else><i class="fa fa-play"></i></template>
                    </button>
                </td>
                <td class="backward">
                    <button class="btn-fa-style" :size="'sm'" @click="goBackward(5)">
                        <i class="fa fa-undo"></i>
                    </button>
                </td>
                <td class="forward">
                    <button class="btn-fa-style" :size="'sm'" @click="goForward(5)">
                        <i class="fa fa-repeat"></i>
                    </button>
                </td>
                <td class="seek-bar">
                    <video-seek-bar></video-seek-bar>
                </td>
                <td class="time">
                    {{ currentTimeString }} - {{ videoEndTimeString }}
                </td>
            </tr>
        </table>
        <table class="st-end-controls">
            <tr>
                <td class="st-controls">
                    <st-end-buttons :is-start="true" :time="videoStartTime"></st-end-buttons>
                </td>
                <td class="st-end-bar">
                    <st-end-input-bar></st-end-input-bar>
                </td>
                <td class="end-controls">
                    <st-end-buttons :is-start="false" :time="videoEndTime"></st-end-buttons>
                </td>
            </tr>
        </table>
    </div>
</template>

<script>
    import moment from 'moment';
    import { mapGetters, mapMutations, mapActions } from 'vuex';
    import VideoSeekBar from './VideoSeekBar';
    import StEndInputBar from './StEndInputBar';
    import StEndButtons from './StEndButtons';

    export default {
        name: 'VideoControls',
        components: {
            VideoSeekBar,
            StEndInputBar,
            StEndButtons,
        },
        data() {
            return {
                playCandidateOnly: true,
            };
        },
        computed: {
            ...mapGetters({
                ready: 'player/getReady',
                playing: 'player/getPlaying',
                showTwitchUI: 'player/getShowTwitchUI',
                videoTime: 'player/getVideoTime',
                videoEndTime: 'player/getVideoEndTime',
                videoStartTime: 'player/getVideoStartTime',
            }),
            currentTimeString() {
                return `${moment(0).startOf('day').second(this.videoTime - this.videoStartTime).format('mm:ss')}`;
            },
            videoEndTimeString() {
                return `${moment(0).startOf('day').second(this.videoEndTime - this.videoStartTime).format('mm:ss')}`;
            },
        },
        methods: {
            playPause() {
                this.setPlaying(!this.playing);
            },
            goBackward(seconds) {
                let newTime;
                if (this.videoTime - seconds > this.videoStartTime) {
                    newTime = this.videoTime - seconds;
                } else newTime = this.videoStartTime;
                this.seekVideo(newTime);
            },
            goForward(seconds) {
                let newTime;
                if (this.videoTime + seconds < this.videoEndTime) {
                    newTime = this.videoTime + seconds;
                } else newTime = this.videoEndTime;
                this.seekVideo(newTime);
            },
            ...mapMutations({
                setPlaying: 'player/setPlaying',
                setShowTwitchUI: 'player/setShowTwitchUI',
            }),
            ...mapActions({
                seekVideo: 'player/seekVideo',
            }),
        },
    };
</script>

<style lang="sass">
    .video-controls-table
        width: 100%
        min-height: 25px
        max-height: 25px
        max-width: 800px
        margin: 0 auto
        border: 0

        .play, .backward, .forward
            max-width: 20px

        td
            text-align: center

        .time
            color: white
            font-size: 12px
            font-weight: 400

    .st-end-controls
        width: 100%
        min-height: 25px
        max-height: 25px
        max-width: 800px
        margin: 0 auto
        border: 0

    .btn-fa-style
        background: transparent
        border: 0
        color: #eee
        &:focus
            border: 0
            background: inherit
            box-shadow: none
        &:active
            border: 0
            background: rgba(255,255,255,0.1)
            box-shadow: none
        &:disabled
            color: rgba(255,255,255,0.1)

    @media screen and (max-width: 992px)
        .btn-fa-style
            font-size: 25px

        .play, .backward, .forward
            width: 6.6%

        .seek-bar
            width: 60%

        .time
            width: 20%

        .st-controls, .end-controls
            width: 20%

        .st-end-bar
            width: 60%

    @media screen and (min-width: 993px)
        .play, .backward, .forward
            width: 5%

        .seek-bar
            width: 70%

        .time
            width: 15%

        .st-controls, .end-controls
            width: 15%

        .st-end-bar
            width: 70%
</style>
