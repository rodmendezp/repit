import { GetHttpRequest, JSONHttpRequest } from '../index';

const config = {
    baseURL: 'http://127.0.0.1:9999/filler/',
};

const localState = {
    games: null,
    streamers: null,
    deliveryTag: null,
};

const getters = {
    getGames: s => s.games,
    getStreamers: s => s.streamers,
    getDeliveryTag: s => s.deliveryTag,
};

const mutations = {
    setGames(s, games) {
        s.games = games;
    },
    setStreamers(s, streamers) {
        s.streamers = streamers;
    },
    setDeliveryTag(s, deliveryTag) {
        s.deliveryTag = deliveryTag;
    },
};

const actions = {
    async requestSetFillerGames({ commit }) {
        return new Promise((resolve, reject) => {
            GetHttpRequest(resolve, reject, `${config.baseURL}games/`);
        }).then((response) => {
            commit('setGames', response.map(x => x.name));
        });
    },
    async requestSetFillerStreamers({ commit }) {
        return new Promise((resolve, reject) => {
            GetHttpRequest(resolve, reject, `${config.baseURL}streamers`);
        }).then((response) => {
            commit('setStreamers', response.map(x => x.name));
        });
    },
    async requestPostJobAck({ state }) {
        return new Promise((resolve, reject) => {
            JSONHttpRequest(resolve, reject, 'POST', {
                baseURL: `${config.baseURL}jobs_available/`,
                data: {
                    delivery_tag: state.deliveryTag,
                },
            });
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
