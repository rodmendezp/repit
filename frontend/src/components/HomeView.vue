<template>
    <div class="main-container full-height">
        <div class="content-container" v-if="status === 'idle'">
            <h3 v-if="user"> Welcome {{ user.first_name }}</h3>
            <div class="container">
                <div class="row form-group row-form-group">
                    <label class="offset-sm-1 col-sm-3 col-form-label">Game</label>
                    <div class="dropdown-container offset-sm-1 col-sm-7">
                        <b-dropdown variant="primary" class="filler-dropdown" :text="gameDropdownText">
                            <b-dropdown-item v-for="game in games" :key="game" :value="game" @click="gameSelected(game)">
                                {{ game }}
                            </b-dropdown-item>
                        </b-dropdown>
                    </div>
                </div>
                <div class="row form-group row-form-group">
                    <label class="offset-sm-1 col-sm-3 col-form-label">Streamer</label>
                    <div class="dropdown-container offset-sm-1 col-sm-7">
                        <b-dropdown variant="primary" class="filler-dropdown" :text="streamerDropdownText">
                            <b-dropdown-item v-for="streamer in defaultAndGameStreamers"
                                             :key="streamer" :value="streamer" @click="streamerSelected(streamer)">
                                {{ streamer }}
                            </b-dropdown-item>
                        </b-dropdown>
                    </div>
                </div>
                <div class="row">
                    <div class="offset-sm-5 col-sm-7 button-container">
                        <button class="btn btn-primary" @click="startLabeling">Start Labeling</button>
                    </div>
                </div>
            </div>
        </div>
        <div v-else-if="status === 'processing'">
            <h3>LOADING</h3>
        </div>
        <div v-else-if="status === 'exception'">
            <h3>{{ exception }}</h3>
        </div>
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
                exception: '',
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

    .main-container
        display: flex
        flex-direction: column
        justify-content: center
        align-items: center

    .content-container
        display: flex
        flex-direction: column
        justify-content: space-evenly
        height: 80%
        width: 80%
        min-width: 400px
        max-width: 600px
        align-items: center
        > h3
            font-size: 4vh

    .filler-dropdown
        background-color: transparent

    .row-form-group
        text-align: center
        > label
            color: white
            font-size: 2.5vh

    .button-container
        text-align: center
        > button
            font-size: 2.5vh
</style>
