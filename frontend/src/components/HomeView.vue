<template>
    <div class="main-container full-height">
        <div class="content-container" v-if="status === 'idle'">
            <h1 class="welcome-title" v-if="user"> Welcome {{ user.first_name }}</h1>
            <div class="container-fluid">
                <div class="row form-group row-form-group">
                    <label class="col-lg-5 col-form-label label-right">Game</label>
                    <div class="offset-lg-1 col-lg-5 dd-container">
                        <div class="btn-group b-dropdown dropdown">
                            <button class="btn btn-primary dropdown-toggle dd-btn" type="button" id="game_dropdown"
                                    data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                {{ gameDropdownText }}
                            </button>
                            <div role="menu" class="dropdown-menu" aria-labelledby="game_dropdown">
                                <a data-boundary="viewport" role="menuitem" class="dropdown-item dd-item" href="#" target="_self"
                                   @click="gameSelected(game)" :value="game" v-for="game in games">
                                    {{ game }}
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="row form-group row-form-group">
                    <label class="offset-lg-1 col-lg-4 col-form-label label-right">Streamer</label>
                    <div class="offset-lg-1 col-lg-4 dd-container">
                        <div class="btn-group b-dropdown dropdown">
                            <button class="btn btn-primary dropdown-toggle dd-btn" type="button" id="streamer_dropdown"
                                    data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                {{ streamerDropdownText }}
                            </button>
                            <div role="menu" class="dropdown-menu" aria-labelledby="streamer_dropdown">
                                <a data-boundary="viewport" role="menuitem" class="dropdown-item dd-item" href="#" target="_self"
                                   @click="streamerSelected(streamer)" :value="streamer" v-for="streamer in defaultAndGameStreamers">
                                    {{ streamer }}
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="offset-lg-6 col-lg-6 button-container">
                        <button class="btn btn-primary" @click="startLabeling">Start Labeling</button>
                    </div>
                </div>
            </div>
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
                longestItem: '',
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
                        this.setHighlightType(null);
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
            setDropdownLongestWidth() {
                console.log();
            },
            ...mapMutations({
                setHost: 'filler/setHost',
                setStatus: 'highlight/setStatus',
                setHighlight: 'highlight/setHighlight',
                setHighlightType: 'highlight/setHighlightType',
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
            if (this.streamers === null) {
                this.requestSetFillerStreamers().then(() => this.setDropdownLongestWidth());
                // this.requestSetFillerStreamers().then(() => this.setLongestDropdownItem());
            }
            // if (this.games !== null && this.streamers !== null) this.setLongestDropdownItem();
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
        width: 100%
        align-items: center
        > h1
            font-size: 4vh

    .dropdown-menu
        max-height: 250px
        overflow-y: auto

    .welcome-title
        text-align: center

    @media screen and (min-width: 992px)
        .dd-container
            display: flex
            justify-content: flex-start

        .label-right
            display: flex
            justify-content: flex-end

        .button-container
            display: flex
            justify-content: flex-start

    .dd-btn, .dd-item
        font-size: 2vh

    .row-form-group
        text-align: center
        > label
            color: white
            font-size: 2vh

    .button-container
        text-align: center
        > button
            font-size: 2.5vh
</style>
