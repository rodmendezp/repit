import Vue from 'vue';
import Vuex from 'vuex';

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
    modules: {},
});

const storeConfig = {
    state,
    getters,
    actions,
    mutations,
    modules: {},
};

export { store as default, storeConfig };
