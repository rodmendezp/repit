// import Vue from 'vue';
import { JSONHttpRequest, GetHttpRequest } from '../index';

const config = {
    baseURL: '/highlight/',
};

const localState = {
    types: null,
    highlight: null,
    status: 'idle',
};

const getters = {
    getTypes: s => s.types,
    getHighlight: s => s.highlight,
    getStatus: s => s.status,
};

const mutations = {
    setTypes(s, types) {
        s.types = types;
    },
    setHighlight(s, highlight) {
        s.highlight = highlight;
    },
    setStatus(s, status) {
        s.status = status;
    },
};

const actions = {
    async postHighlight() {
        return new Promise((resolve, reject) => {
            JSONHttpRequest(resolve, reject, 'POST', {
                baseURL: `${config.baseURL}highlight/`,

            });
        });
    },
    async putHighlight(highlight) {
        return new Promise((resolve, reject) => {
            JSONHttpRequest(resolve, reject, 'PUT', {
                baseURL: `${config.baseURL}highlight/${highlight.pop('id')}`,
                data: highlight,
            });
        });
    },
    async getTypesDB({ commit }) {
        return new Promise((resolve, reject) => {
            GetHttpRequest(resolve, reject, `${config.baseURL}type`);
        }).then((response) => {
            commit('setTypes', response.map(x => x.name));
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
