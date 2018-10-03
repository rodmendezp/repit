<template>
    <div>
        <table class="video-controls">
            <tr>
                <td class="play" width="5%">
                    <button class="btn-style" :disabled="!ready" :size="'sm'" @click="playPause">
                        <template v-if="playing"><i class="fa fa-pause"></i></template>
                        <template v-else><i class="fa fa-play"></i></template>
                    </button>
                </td>
                <td class="backward" width="5%">
                    <button class="btn-style" :size="'sm'" @click="goBackward(5)">
                        <i class="fa fa-undo"></i>
                    </button>
                </td>
                <td class="forward" width="5%"  @click="goForward(5)">
                    <button class="btn-style" :size="'sm'" @click="goForward(5)">
                        <i class="fa fa-repeat"></i>
                    </button>
                </td>
                <td class="seek-bar" width="70%">
                    <video-seek-bar></video-seek-bar>
                </td>
                <td class="time" width="15%">
                    {{ currentTimeString }} - {{ videoEndTimeString }}
                </td>
            </tr>
            <tr>
                <td width="5%"></td>
                <td width="5%"></td>
                <td width="5%"></td>
                <td width="70%">
                    <st-end-input-bar></st-end-input-bar>
                </td>
                <td width="15%"></td>
            </tr>
        </table>
        <table class="extra-controls">
            <tr>
                <td width="30%"></td>
                <!--<td width="20%"></td>-->
                <td width="40%">
                    <button @click="setShowTwitchUI(!showTwitchUI)">
                        <template v-if="showTwitchUI">Hide Twitch UI</template>
                        <template v-else>Show Twitch UI</template>
                    </button>
                </td>
                <!--<td width="20%"></td>-->
                <td width="30%"></td>
            </tr>
        </table>
    </div>
</template>

<script>
    import moment from 'moment';
    import { mapGetters, mapMutations, mapActions } from 'vuex';
    import VideoSeekBar from './VideoSeekBar';
    import StEndInputBar from './StEndInputBar';

    export default {
        name: 'VideoControls',
        components: {
            VideoSeekBar,
            StEndInputBar,
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
    .video-controls
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

        .fa
            color: #eee

        .btn-style, .btn-style button
            background: transparent !important
            border: 0 !important
            &:focus
                border: 0
                background: inherit
                box-shadow: none !important
            &:active
                border: 0
                background: rgba(255,255,255,0.1)
                box-shadow: none !important

    .extra-controls
        width: 100%
        margin-top: 5px

</style>
