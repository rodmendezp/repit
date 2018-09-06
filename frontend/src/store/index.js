import Vue from 'vue';
import Vuex from 'vuex';
import highlight from './modules/highlight';

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
    },
});

const storeConfig = {
    state,
    getters,
    actions,
    mutations,
    modules: {
        highlight,
    },
};

export { store as default, storeConfig };
