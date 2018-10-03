<template>
    <div>
        <div class="twitch-player" :id="`Twitch-Player-${uid}`"></div>
        <div class="video-controls">
            <video-controls></video-controls>
        </div>
    </div>
</template>

<script>
    import { loadScript } from '@/mixins/scriptUtils';
    import { mapGetters, mapMutations, mapActions } from 'vuex';
    import VideoControls from './VideoControls';

    export default {
        name: 'TwitchPlayer',
        props: {
            videoId: { type: Number },
            stTime: { type: Number },
            endTime: { type: Number },
        },
        components: {
            VideoControls,
        },
        data() {
            return {
                player: null,
                options: {},
                seekAtInstantPlay: true,
                changeStatus: false,
                iframeTwitch: null,
                destroying: false,
            };
        },
        computed: {
            ...mapGetters({
                playing: 'player/getPlaying',
                seekTime: 'player/getSeekTime',
                videoTime: 'player/getVideoTime',
                videoStartTime: 'player/getVideoStartTime',
                videoEndTime: 'player/getVideoEndTime',
                showTwitchUI: 'player/getShowTwitchUI',
                videoInfo: 'twitchdata/getVideoInfo',
            }),
            uid() {
                return this._uid;
            },
        },
        methods: {
            loadScript,
            playUpdateTimeSeekLoop() {
                // Stop looping if the component is going to be destroyed
                if (this.destroying) return;
                // Twitch Player getCurrentTime():Float
                const currTime = this.player.getCurrentTime();
                if (this.videoStartTime <= currTime && currTime < this.videoEndTime) {
                    this.setVideoTime(currTime);
                    setTimeout(this.playUpdateTimeSeekLoop, 100);
                } else {
                    this.player.seek(this.videoStartTime);
                    this.setVideoTime(this.videoStartTime);
                    this.setPlaying(false);
                }
            },
            secondsToTimeString(seconds) {
                let restStTime = seconds;
                let timeString = '';
                const timeChars = ['h', 'm', 's'];
                for (let i = 0; i < 3; i += 1) {
                    timeString += Math.trunc(restStTime / (60 ** (2 - i))).toString() + timeChars[i];
                    restStTime %= (60 ** (2 - i));
                }
                return timeString;
            },
            timeStringToSecs(timeString) {
                let seconds = 0;
                for (let i = 0; i < 3; i += 1) {
                    seconds += parseInt(timeString.substring(3 * i, (3 * i) + 2), 10) * (60 ** (2 - i));
                }
                return seconds;
            },
            ...mapMutations({
                setReady: 'player/setReady',
                setPlaying: 'player/setPlaying',
                setSeekTime: 'player/setSeekTime',
                setVideoTime: 'player/setVideoTime',
                setVideoLength: 'player/setVideoLength',
                setVideoStartTime: 'player/setVideoStartTime',
                setVideoEndTime: 'player/setVideoEndTime',
            }),
            ...mapActions({
                playRepitUI: 'player/playRepitUI',
                pauseRepitUI: 'player/pauseRepitUI',
                seekVideo: 'player/seekVideo',
            }),
        },
        mounted() {
            this.options.video = this.videoId;
            this.options.time = this.secondsToTimeString(this.stTime);
            if (!this.showTwitchUI) this.options.controls = false;
            this.options.autoplay = false;
            if (this.videoInfo !== null) this.setVideoLength(this.timeStringToSecs(this.videoInfo.length));
            this.setVideoTime(parseFloat(this.stTime));
            this.setVideoStartTime(parseFloat(this.stTime));
            this.setVideoEndTime(parseFloat(this.endTime));
            this.loadScript('http://player.twitch.tv/js/embed/v1.js', 'Twitch').then((Twitch) => {
                this.Twitch = Twitch;
                this.player = new Twitch.Player(`Twitch-Player-${this.uid}`, this.options);
                this.player.setVolume(1);
                this.player.addEventListener(Twitch.Player.READY, () => {
                    this.iframeTwitch = this.player._bridge._iframe;
                    this.setReady(true);
                });
                this.player.addEventListener(Twitch.Player.PLAY, () => {
                    this.playRepitUI();
                    this.playUpdateTimeSeekLoop();
                    console.log('Twitch Player PLAY');
                });
                this.player.addEventListener(Twitch.Player.PAUSE, () => {
                    this.pauseRepitUI();
                    console.log('Twitch Player PAUSE');
                });
                this.player.addEventListener(Twitch.Player.PLAYING, () => {
                    // this.playRepitUI();
                    console.log('Twitch Player PLAYING');
                });
                this.player.addEventListener(Twitch.Player.VIDEO_READY, () => {
                    // console.log('Twitch Player VIDEO_READY');
                });
                this.player.addEventListener(Twitch.Player.PLAYBACK_BLOCKED, () => {
                    // console.log('Twitch Player PLAYBACK_BLOCKED');
                });
                this.player.addEventListener(Twitch.Player.ERROR, () => {
                    // console.log('Twitch Player ERROR');
                });
                this.player.addEventListener(Twitch.Player.ENDED, () => {
                    // console.log('Twitch Player ENDED');
                });
                this.player.addEventListener(Twitch.Player.PLAYBACK_BLOCKED, () => {
                    // console.log('Twitch Player PLAYBACK_BLOCKED');
                });
            });
        },
        beforeDestroy() {
            this.destroying = true;
        },
        watch: {
            playing(isPlaying) {
                if (isPlaying) {
                    this.player.play();
                } else this.player.pause();
            },
            seekTime(newValue, oldValue) {
                if (newValue !== -1 && oldValue === -1) {
                    // Twitch Player seek(timestamp:Float)
                    this.player.seek(newValue);
                    this.setSeekTime(-1);
                }
            },
            showTwitchUI(show) {
                this.iframeTwitch.src = show ?
                    this.iframeTwitch.src.replace('&!controls', '') : `${this.iframeTwitch.src}&!controls`;
            },
            videoInfo() {
                if (this.videoInfo !== null) this.setVideoLength(this.timeStringToSecs(this.videoInfo.length));
            },
            videoStartTime() {
                if (this.videoStartTime > this.videoTime) this.seekVideo(this.videoStartTime);
            },
            videoEndTime() {
                if (this.videoTime > this.videoEndTime) this.seekVideo(this.videoEndTime);
            },
        },
    };
</script>

<style lang="sass">
    /*.twitch-player*/
        /*width: 400px*/
        /*height: 400px*/

</style>
