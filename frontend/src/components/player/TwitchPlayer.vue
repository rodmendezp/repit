<template>
    <div class="twitch-player" :id="`Twitch-Player-${uid}`"></div>
</template>

<script>
    import { loadScript } from '@/mixins/scriptUtils';
    import { mapGetters } from 'vuex';

    export default {
        name: 'TwitchPlayer',
        props: {
            videoId: { type: String },
            stTime: { type: String },
            endTime: { type: String },
        },
        components: {},
        data() {
            return {
                player: null,
                options: {},
                seekAtInstantPlay: true,
                changeStatus: false,
            };
        },
        computed: {
            ...mapGetters({
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
        },
        mounted() {
            this.options.video = this.videoId;
            this.loadScript('http://player.twitch.tv/js/embed/v1.js', 'Twitch').then((Twitch) => {
                // console.log('Twitch Script Loaded');
                this.Twitch = Twitch;
                this.player = new Twitch.Player(`Twitch-Player-${this.uid}`, this.options);
                this.player.setVolume(0.5);
                this.player.addEventListener(Twitch.Player.READY, () => {
                    // console.log('Twitch Player READY');
                });
                this.player.addEventListener(Twitch.Player.PLAY, () => {
                    // console.log('Twitch Player PLAY');
                });
                this.player.addEventListener(Twitch.Player.PAUSE, () => {
                    // console.log('Twitch Player PAUSE');
                });
                this.player.addEventListener(Twitch.Player.PLAYING, () => {
                    // console.log('Twitch Player PLAYING');
                    if (this.seekAtInstantPlay) {
                        this.player.seek(this.stTime);
                        this.seekAtInstantPlay = false;
                    } else {
                        const currTime = this.player.getCurrentTime();
                        if (currTime < this.stTime || currTime > this.endTime) {
                            this.player.seek(this.stTime);
                            this.player.pause();
                        } else {
                            const timeLeft = (Math.round(this.endTime - currTime) + 1) * 1000;
                            setTimeout(this.checkPlayerTime, timeLeft);
                        }
                    }
                });
            });
        },
    };
</script>

<style lang="sass">
    .twitch-player
        width: 400px
        height: 400px

</style>
