import Vue from 'vue';
import Vuex from 'vuex';
import highlight from './modules/highlight';
import player from './modules/player';

Vue.use(Vuex);

const state = {
    user: null,
};

const mutations = {
    setUser(s, user) {
        s.user = user;
    },
};

const getters = {
    getUser: s => s.user,
};

const actions = {};

const store = new Vuex.Store({
    state,
    getters,
    actions,
    mutations,
    modules: {
        highlight,
        player,
    },
});

const storeConfig = {
    state,
    getters,
    actions,
    mutations,
    modules: {
        highlight,
        player,
    },
};

export { store as default, storeConfig };
