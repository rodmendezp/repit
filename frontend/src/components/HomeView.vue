<template>
    <div class="row full-height align-items-center">
        <div class="col"></div>
        <div style="text-align: center" class="col" v-if="status === 'idle'">
            <h1 v-if="user"> Welcome {{ user.first_name }}</h1>
            <div class="form-group start-label-form">
                <div class="form-block">
                    <label>Game</label>
                    <b-dropdown variant="primary" class="btn-primary filler-dropdown" :text="gameDropdownText">
                        <b-dropdown-item v-for="game in games"
                                         :key="game" :value="game" @click="gameSelected(game)">
                            {{ game }}
                        </b-dropdown-item>
                    </b-dropdown>
                </div>
                <div class="form-block">
                    <label>Streamer</label>
                    <b-dropdown variant="primary" class="btn-primary filler-dropdown" :text="streamerDropdownText">
                        <b-dropdown-item v-for="streamer in defaultAndGameStreamers"
                                         :key="streamer" :value="streamer" @click="streamerSelected(streamer)">
                            {{ streamer }}
                        </b-dropdown-item>
                    </b-dropdown>
                </div>
            </div>
            <button class="btn btn-primary" @click="startLabeling">Start Labeling</button>
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

    export default {
        name: 'HomeView',
        components: {
            bDropdown,
            bDropdownItem,
        },
        data() {
            return {
                labelOptions: {
                    game: null,
                    streamer: null,
                },
            };
        },
        methods: {
            startLabeling() {
                this.setStatus('processing');
                this.setGame(this.labelOptions.game);
                if (this.labelOptions.streamer !== null) {
                    this.setStreamer(this.labelOptions.streamer);
                    this.setUser(this.user.email);
                }
                const params = {
                    game: this.labelOptions.game,
                    streamer: this.labelOptions.streamer === null ? '' : this.labelOptions.streamer,
                    user: this.labelOptions.streamer === null ? '' : this.user.email,
                };
                this.requestTaskLoop(params);
            },
            requestTaskLoop(params) {
                console.log('requestTaskLoop');
                this.requestGetTask(params).then((response) => {
                    console.log(response);
                    if (response.task !== undefined) {
                        this.setDeliveryTag(response.task.delivery_tag);
                        delete response.task.delivery_tag;
                        this.setHighlight(response.task);
                        this.requestSetVideoInfo(response.task.video_id);
                        this.$router.push('/label/');
                    } else if (response.message !== undefined && response.message !== 'Something went wrong') {
                        setTimeout(this.requestTaskLoop, 5000, params);
                    } else {
                        console.log('There was an error somewhere');
                    }
                });
            },
            gameSelected(game) {
                this.labelOptions.game = game;
                this.requestSetGameStreamers(game);
                this.requestSetGameDefaultsStreamers(game);
            },
            streamerSelected(streamer) {
                this.labelOptions.streamer = streamer;
            },
            ...mapMutations({
                setHost: 'filler/setHost',
                setStatus: 'highlight/setStatus',
                setHighlight: 'highlight/setHighlight',
                setVideoInfo: 'twitchdata/setVideoInfo',
                setDeliveryTag: 'filler/setDeliveryTag',
                setGame: 'label/setGame',
                setStreamer: 'label/setStreamer',
                setUser: 'label/setUser',
            }),
            ...mapActions({
                requestGetTask: 'filler/requestGetTask',
                requestSetFillerGames: 'filler/requestSetFillerGames',
                requestSetFillerStreamers: 'filler/requestSetFillerStreamers',
                requestSetGameStreamers: 'filler/requestSetGameStreamers',
                requestSetGameDefaultsStreamers: 'filler/requestSetGameDefaultsStreamers',
                requestSetVideoInfo: 'twitchdata/requestSetVideoInfo',
            }),
        },
        computed: {
            ...mapGetters({
                user: 'getUser',
                webSocket: 'getWebSocket',
                status: 'highlight/getStatus',
                games: 'filler/getGames',
                streamers: 'filler/getStreamers',
                gameStreamers: 'filler/getGameStreamers',
            }),
            defaultAndGameStreamers() {
                const allStreamers = [];
                const streamersSet = new Set();
                if (this.streamers) {
                    for (let i = 0; i < this.streamers.length; i += 1) {
                        allStreamers.push(this.streamers[i]);
                        streamersSet.add(this.streamers[i]);
                    }
                }
                if (this.gameStreamers) {
                    for (let i = 0; i < this.gameStreamers.length; i += 1) {
                        if (!streamersSet.has(this.gameStreamers[i])) {
                            allStreamers.push(this.gameStreamers[i]);
                        }
                    }
                }
                return allStreamers;
            },
            gameDropdownText() {
                return this.labelOptions.game !== null ? this.labelOptions.game : '---------------';
            },
            streamerDropdownText() {
                return this.labelOptions.streamer !== null ? this.labelOptions.streamer : '---------------';
            },
        },
        mounted() {
            this.setHost(window.location.host);
            if (this.games === null) this.requestSetFillerGames();
            if (this.streamers === null) this.requestSetFillerStreamers();
        },
    };
</script>

<style scoped lang="sass">
    @import '~@/styles/app/main.scss';

    .start-label-form
        max-width: 600px
        margin: 20px auto 30px

    .form-block
        margin-top: 5px
        margin-bottom: 5px

    .form-block label
        display: inline-block
        width: 100px
        text-align: right
        color: white

    .filler-dropdown
        margin-left: 10px
        background-color: transparent

</style>
