import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

const state = {};

const mutations = {};

const getters = {};

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
