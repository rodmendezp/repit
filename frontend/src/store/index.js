import Vue from 'vue';
import Vuex from 'vuex';
import highlight from './modules/highlight';
import player from './modules/player';
import filler from './modules/filler';
import label from './modules/label';

Vue.use(Vuex);

function JSONHttpRequest(resolve, reject, method, params) {
    const xhr = new XMLHttpRequest();
    xhr.open(method, params.baseURL, true);
    xhr.setRequestHeader('X-CSRFToken', params.csrfToken);
    xhr.setRequestHeader('Content-type', 'application/json; charset=utf-8');
    xhr.onreadystatechange = () => {
        if (xhr.readyState === 4) {
            let response;
            if (xhr.getResponseHeader('content-type') === 'application/json') {
                response = JSON.parse(xhr.response);
            } else response = xhr.response;
            if (response.status === 'ERROR') reject();
            else resolve(response);
        }
    };
    xhr.onerror = () => { reject(); };
    xhr.send(JSON.stringify(params.data));
}

function GetHttpRequest(resolve, reject, url) {
    const xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.onreadystatechange = () => {
        if (xhr.readyState === 4) {
            if (xhr.status !== 200) {
                reject();
                return;
            }
            const response = JSON.parse(xhr.response);
            if (response.status === 'ERROR') reject();
            else resolve(response);
        }
    };
    xhr.onerror = () => { reject(); };
    xhr.send();
}

const state = {
    user: null,
    webSocket: null,
};

const mutations = {
    setUser(s, user) {
        s.user = user;
    },
    setWebSocket(s, webSocket) {
        s.webSocket = webSocket;
    },
};

const getters = {
    getUser: s => s.user,
    getWebSocket: s => s.webSocket,
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
        filler,
        label,
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
        filler,
        label,
    },
};

export { store as default, storeConfig };
export { JSONHttpRequest, GetHttpRequest };
