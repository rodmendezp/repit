import { GetHttpRequest, JSONHttpRequest } from '../index';

const localState = {
    games: null,
    streamers: null,
    gameStreamers: null,
    deliveryTag: null,
    host: null,
    csrfmiddlewaretoken: '',
};

const getters = {
    getHost: s => s.host,
    getGames: s => s.games,
    getStreamers: s => s.streamers,
    getGameStreamers: s => s.gameStreamers,
    getDeliveryTag: s => s.deliveryTag,
};

const mutations = {
    setHost(s, host) {
        s.host = host;
    },
    setGames(s, games) {
        s.games = games;
    },
    setStreamers(s, streamers) {
        s.streamers = streamers;
    },
    setGameStreamers(s, gameStreamers) {
        s.gameStreamers = gameStreamers;
    },
    setDeliveryTag(s, deliveryTag) {
        s.deliveryTag = deliveryTag;
    },
    setCSRF(s, csrfmiddlewaretoken) {
        s.csrfmiddlewaretoken = csrfmiddlewaretoken;
    },
};

const actions = {
    async requestSetFillerGames({ state, commit }) {
        return new Promise((resolve, reject) => {
            GetHttpRequest(resolve, reject, `http://${state.host}/backend/filler_game/`);
        }).then((response) => {
            commit('setGames', response.map(x => x.name));
        });
    },
    async requestSetFillerStreamers({ state, commit }) {
        return new Promise((resolve, reject) => {
            GetHttpRequest(resolve, reject, `http://${state.host}/backend/filler_streamer/`);
        }).then((response) => {
            commit('setStreamers', response.map(x => x.name));
        });
    },
    async requestPostJobAck({ state, commit }) {
        return new Promise((resolve, reject) => {
            if (!state.csrfmiddlewaretoken) commit('setCSRF', document.getElementsByName('csrfmiddlewaretoken')[0].value);
            JSONHttpRequest(resolve, reject, 'POST', {
                baseURL: `http://${state.host}/backend/task/`,
                csrfToken: state.csrfmiddlewaretoken,
                data: {
                    delivery_tag: state.deliveryTag,
                },
            });
        });
    },
    async requestSetGameStreamers({ state, commit }, game) {
        return new Promise((resolve, reject) => {
            GetHttpRequest(resolve, reject, `http://${state.host}/backend/filler_streamer/?game=${encodeURI(game)}`);
        }).then((response) => {
            commit('setGameStreamers', response.streamers);
        });
    },
    async requestSetGameDefaultsStreamers({ state, commit }, game) {
        return new Promise((resolve, reject) => {
            GetHttpRequest(resolve, reject, `http://${state.host}/backend/filler_streamer/?game_defaults=${encodeURI(game)}`);
        }).then((response) => {
            commit('setStreamers', response.streamers);
        });
    },
    async requestGetTask({ state }, params) {
        return new Promise((resolve, reject) => {
            GetHttpRequest(resolve, reject, `http://${state.host}/backend/task/?game=${params.game}&streamer=${params.streamer}&user=${params.user}`);
        });
    },
};

export default {
    namespaced: true,
    state: localState,
    getters,
    mutations,
    actions,
};
