<template>
    <table class="video-controls">
        <tr>
            <td class="play" width="5%">
                <button class="btn-style" :disabled="!ready" :size="'sm'" @click="playPause">
                    <template v-if="playing"><i class="fa fa-pause"></i></template>
                    <template v-else><i class="fa fa-play"></i></template>
                </button>
            </td>
            <td class="time" width="15%">
                {{ currentTimeString }}
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
            <td class="seek-bar" width="45%">
                <video-seek-bar></video-seek-bar>
            </td>
            <!--<td class="volume" width="5%">-->

            <!--</td>-->
            <td width="35%">
                <button @click="setShowTwitchUI(!showTwitchUI)">
                    <template v-if="showTwitchUI">Hide Twitch UI</template>
                    <template v-else>Show Twitch UI</template>
                </button>
            </td>
        </tr>
    </table>
</template>

<script>
    import moment from 'moment';
    import { mapGetters, mapMutations } from 'vuex';
    import VideoSeekBar from './VideoSeekBar';

    export default {
        name: 'VideoControls',
        components: {
            VideoSeekBar,
        },
        data() {
            return {};
        },
        computed: {
            ...mapGetters({
                ready: 'player/getReady',
                playing: 'player/getPlaying',
                showTwitchUI: 'player/getShowTwitchUI',
                videoTime: 'player/getVideoTime',
            }),
            currentTimeString() {
                return `${moment(0).startOf('day').second(this.videoTime).format('HH:mm:ss')}`;
            },
        },
        methods: {
            playPause() {
                this.setPlaying(!this.playing);
            },
            goBackward(seconds) {
                console.log(seconds);
            },
            goForward(seconds) {
                console.log(seconds);
            },
            ...mapMutations({
                setPlaying: 'player/setPlaying',
                setShowTwitchUI: 'player/setShowTwitchUI',
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



</style>
