import { GetHttpRequest } from '../index';

const config = {
    baseURL: 'http://127.0.0.1:9999/filler/',
};

const localState = {
    games: null,
    streamers: null,
};

const getters = {
    getGames: s => s.games,
    getStreamers: s => s.streamers,
};

const mutations = {
    setGames(s, games) {
        s.games = games;
    },
    setStreamers(s, streamers) {
        s.streamers = streamers;
    },
};

const actions = {
    async getFillerGames({ commit }) {
        return new Promise((resolve, reject) => {
            GetHttpRequest(resolve, reject, `${config.baseURL}games/`);
        }).then((response) => {
            commit('setGames', response.map(x => x.name));
        });
    },
    async getFillerStreamers({ commit }) {
        return new Promise((resolve, reject) => {
            GetHttpRequest(resolve, reject, `${config.baseURL}streamers`);
        }).then((response) => {
            commit('setStreamers', response.map(x => x.name));
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
