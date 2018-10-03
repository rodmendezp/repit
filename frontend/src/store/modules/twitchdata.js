import { GetHttpRequest } from '../index';

const config = {
    baseURL: '/twitchdata/',
};

const localState = {
    videoInfo: null,
};

const getters = {
    getVideoInfo: s => s.videoInfo,
};

const mutations = {
    setVideoInfo(s, videoInfo) {
        s.videoInfo = videoInfo;
    },
};

const actions = {
    async requestSetVideoInfo({ commit }, videoTwid) {
        return new Promise((resolve, reject) => {
            GetHttpRequest(resolve, reject, `${config.baseURL}video/?twid=${videoTwid}`);
        }).then((response) => {
            if (response.length === 1) commit('setVideoInfo', response[0]);
            else console.log(`Something wrong with request ${config.baseURL}video/?twid=${videoTwid}`);
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
