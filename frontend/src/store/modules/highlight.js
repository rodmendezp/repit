// import Vue from 'vue';
import { JSONHttpRequest, GetHttpRequest } from '../index';

const config = {
    baseURL: '/highlight/',
};

const localState = {
    types: null,
    highlight: null,
    status: 'idle',
    csrfmiddlewaretoken: '',
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
    setCSRF(s, csrfmiddlewaretoken) {
        s.csrfmiddlewaretoken = csrfmiddlewaretoken;
    },
    setHighlightType(s, type) {
        s.highlight.type = type;
    },
    setHighlightStart(s, start) {
        s.highlight.st_time = start;
    },
    setHighlightEnd(s, end) {
        s.highlight.end_time = end;
    },
};

const actions = {
    async postHighlight({ state, commit }, data) {
        return new Promise((resolve, reject) => {
            if (!state.csrfmiddlewaretoken) commit('setCSRF', document.getElementsByName('csrfmiddlewaretoken')[0].value);
            JSONHttpRequest(resolve, reject, 'POST', {
                baseURL: `${config.baseURL}highlight/`,
                csrfToken: state.csrfmiddlewaretoken,
                data: {
                    video: data.video_id,
                    start: data.st_time,
                    end: data.end_time,
                    type: data.type,
                },
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
