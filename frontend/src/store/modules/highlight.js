// import Vue from 'vue';

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

const config = {
    baseURL: '/highlight/',
};

const localState = {
    types: null,
};

const getters = {
    getTypes: s => s.types,
};

const mutations = {
    setTypes(s, types) {
        s.types = types;
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
