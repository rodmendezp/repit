const localState = {
    ready: false,
    playing: false,
    buffered: false,
    seekTime: -1,
    videoTime: 0,
    videoLength: 1,
    videoStartTime: 0,
    videoEndTime: 1,
    showTwitchUI: true,
    extraTimeLeft: 0,
    extraTimeRight: 0,
};

const getters = {
    getReady: s => s.ready,
    getPlaying: s => s.playing,
    getBuffered: s => s.buffered,
    getSeekTime: s => s.seekTime,
    getVideoTime: s => s.videoTime,
    getVideoLength: s => s.videoLength,
    getVideoStartTime: s => s.videoStartTime,
    getVideoEndTime: s => s.videoEndTime,
    getShowTwitchUI: s => s.showTwitchUI,
    getExtraTimeLeft: s => s.extraTimeLeft,
    getExtraTimeRight: s => s.extraTimeRight,
};

const mutations = {
    setReady(s, ready) {
        s.ready = ready;
    },
    setPlaying(s, playing) {
        s.playing = playing;
    },
    setBuffered(s, buffered) {
        s.buffered = buffered;
    },
    setSeekTime(s, seekTime) {
        s.seekTime = seekTime;
    },
    setVideoTime(s, videoTime) {
        s.videoTime = videoTime;
    },
    setVideoLength(s, videoLength) {
        s.videoLength = videoLength;
    },
    setVideoStartTime(s, videoStartTime) {
        s.videoStartTime = videoStartTime;
    },
    setVideoEndTime(s, videoEndTime) {
        s.videoEndTime = videoEndTime;
    },
    setShowTwitchUI(s, showTwitchUI) {
        s.showTwitchUI = showTwitchUI;
    },
    setExtraTimeLeft(s, extraTimeLeft) {
        s.extraTimeLeft = extraTimeLeft;
    },
    setExtraTimeRight(s, extraTimeRight) {
        s.extraTimeRight = extraTimeRight;
    },
};

const actions = {
    seekVideo({ commit }, newTime) {
        commit('setBuffered', false);
        commit('setSeekTime', newTime);
    },
    playRepitUI({ state, commit }) {
        if (state.playing) return;
        commit('setPlaying', true);
    },
    pauseRepitUI({ state, commit }) {
        if (!state.playing) return;
        commit('setPlaying', false);
    },
};

export default {
    namespaced: true,
    state: localState,
    getters,
    mutations,
    actions,
};
