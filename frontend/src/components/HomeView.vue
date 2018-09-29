<template>
    <div class="row full-height align-items-center">
        <div class="col"></div>
        <div style="text-align: center" class="col" v-if="status === 'idle'">
            <h1 v-if="user"> Welcome {{ user.first_name }}</h1>
            <div class="form-group start-label-form">
                <div class="form-block">
                    <label>Game</label>
                    <b-dropdown variant="primary" class="btn-primary filler-dropdown" :text="labelOptions.game">
                        <b-dropdown-item v-for="game in games"
                                         :key="game" :value="game" @click="labelOptions.game = game">
                            {{ game }}
                        </b-dropdown-item>
                    </b-dropdown>
                </div>
                <div class="form-block">
                    <label>Streamer</label>
                    <b-dropdown variant="primary" class="btn-primary filler-dropdown" :text="labelOptions.streamer">
                        <b-dropdown-item v-for="streamer in streamers"
                                         :key="streamer" :value="streamer" @click="labelOptions.streamer = streamer">
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
    import ReconnectingWebSocket from 'reconnecting-websocket';

    export default {
        name: 'HomeView',
        components: {
            bDropdown,
            bDropdownItem,
        },
        data() {
            return {
                labelOptions: {
                    game: '---------------',
                    streamer: '---------------',
                },
            };
        },
        methods: {
            startLabeling() {
                this.setStatus('processing');
                this.webSocket.send(JSON.stringify({
                    message: 'GET_HIGHLIGHT',
                }));
            },
            connectToWebSocket() {
                const socketURL = `ws://${window.location.host}/ws/chat/`;
                const websocket = new ReconnectingWebSocket(socketURL);
                websocket.onopen = this.onOpen;
                websocket.onclose = this.onClose;
                websocket.onmessage = this.onMessage;
                websocket.onerror = this.onError;
                this.setWebSocket(websocket);
            },
            onOpen(event) {
                console.log('Connection opened.', event.data);
            },
            onClose(event) {
                console.log('Connection closed.', event.data);
                // Try and Reconnect after five seconds
                setTimeout(this.connectToWebSocket, 5000);
            },
            onMessage(event) {
                const message = JSON.parse(event.data);
                console.log('onMessage = ', message);
                if (message.message === 'ERROR') {
                    console.log('There was an error');
                } else if (message.message === 'LOADING') {
                    setTimeout(this.startLabeling, 5000);
                } else {
                    this.setHighlight(message.message);
                    this.$router.push('/label/');
                }
            },
            onError(event) {
                console.log('An error occured:', event.data);
            },
            ...mapMutations({
                setWebSocket: 'setWebSocket',
                setHighlight: 'highlight/setHighlight',
                setStatus: 'highlight/setStatus',
            }),
            ...mapActions({
                getFillerGames: 'filler/getFillerGames',
                getFillerStreamers: 'filler/getFillerStreamers',
            }),
        },
        computed: {
            ...mapGetters({
                user: 'getUser',
                webSocket: 'getWebSocket',
                status: 'highlight/getStatus',
                games: 'filler/getGames',
                streamers: 'filler/getStreamers',
            }),
        },
        mounted() {
            this.connectToWebSocket();
            if (this.games === null) this.getFillerGames();
            if (this.streamers === null) this.getFillerStreamers();
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
