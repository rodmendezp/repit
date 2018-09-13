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
    import { mapGetters, mapMutations } from 'vuex';
    import VideoControls from './VideoControls';

    export default {
        name: 'TwitchPlayer',
        props: {
            videoId: { type: String },
            stTime: { type: String },
            endTime: { type: String },
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
            };
        },
        computed: {
            ...mapGetters({
                playing: 'player/getPlaying',
                seekTime: 'player/getSeekTime',
                showTwitchUI: 'player/getShowTwitchUI',
            }),
            uid() {
                return this._uid;
            },
        },
        methods: {
            loadScript,
            checkPlayerTime() {
                const currTime = this.player.getCurrentTime();
                if (currTime < this.stTime || currTime > this.endTime) {
                    this.player.seek(this.stTime);
                    this.player.pause();
                }
            },
            playSeekLoop() {
                if (this.seekAtInstantPlay) {
                    this.player.seek(this.stTime);
                    this.seekAtInstantPlay = false;
                } else {
                    const currTime = this.player.getCurrentTime();
                    if (currTime < this.stTime || currTime > this.endTime) {
                        this.player.seek(this.stTime);
                        this.setVideoTime(this.stTime);
                        this.setPlaying(false);
                    } else {
                        const timeLeft = (Math.round(this.endTime - currTime) + 1) * 1000;
                        setTimeout(this.checkPlayerTime, timeLeft);
                    }
                }
            },
            playUpdateTimeSeekLoop() {
                // console.log('playUpdateTimeSeekLoop');
                // Twitch Player getCurrentTime():Float
                const currTime = this.player.getCurrentTime();
                if (this.stTime <= currTime && currTime < this.endTime) {
                    this.setVideoTime(currTime);
                    setTimeout(this.playUpdateTimeSeekLoop, 100);
                } else {
                    this.player.seek(this.stTime);
                    this.setVideoTime(this.stTime);
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
            ...mapMutations({
                setReady: 'player/setReady',
                setPlaying: 'player/setPlaying',
                setSeekTime: 'player/setSeekTime',
                setVideoTime: 'player/setVideoTime',
                setVideoStartTime: 'player/setVideoStartTime',
                setVideoEndTime: 'player/setVideoEndTime',
            }),
        },
        mounted() {
            this.options.video = this.videoId;
            this.options.time = this.secondsToTimeString(this.stTime);
            if (!this.showTwitchUI) this.options.controls = false;
            this.options.autoplay = false;
            this.setVideoTime(parseFloat(this.stTime));
            this.setVideoStartTime(parseFloat(this.stTime));
            this.setVideoEndTime(parseFloat(this.endTime));
            this.loadScript('http://player.twitch.tv/js/embed/v1.js', 'Twitch').then((Twitch) => {
                this.Twitch = Twitch;
                this.player = new Twitch.Player(`Twitch-Player-${this.uid}`, this.options);
                this.player.setVolume(1);
                this.player.addEventListener(Twitch.Player.READY, () => {
                    console.log('Twitch Player READY');
                    this.iframeTwitch = this.player._bridge._iframe;
                    this.setReady(true);
                    console.log(Twitch);
                });
                this.player.addEventListener(Twitch.Player.PLAY, () => {
                    console.log('Twitch Player PLAY');
                    this.playUpdateTimeSeekLoop();
                });
                this.player.addEventListener(Twitch.Player.PAUSE, () => {
                    console.log('Twitch Player PAUSE');
                });
                this.player.addEventListener(Twitch.Player.PLAYING, () => {
                    console.log('Twitch Player PLAYING');
                });
                this.player.addEventListener(Twitch.Player.VIDEO_READY, () => {
                    console.log('Twitch Player VIDEO_READY');
                });
                this.player.addEventListener(Twitch.Player.PLAYBACK_BLOCKED, () => {
                    console.log('Twitch Player PLAYBACK_BLOCKED');
                });
                this.player.addEventListener(Twitch.Player.ERROR, () => {
                    console.log('Twitch Player ERROR');
                });
                this.player.addEventListener(Twitch.Player.ENDED, () => {
                    console.log('Twitch Player ENDED');
                });
                this.player.addEventListener(Twitch.Player.PLAYBACK_BLOCKED, () => {
                    console.log('Twitch Player PLAYBACK_BLOCKED');
                });
            });
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
                if (show) {
                    this.iframeTwitch.src = this.iframeTwitch.src.replace('&!controls', '');
                } else {
                    this.iframeTwitch.src += '&!controls';
                }
            },
        },
    };
</script>

<style lang="sass">
    .twitch-player
        width: 400px
        height: 400px

</style>
