const localState = {
    ready: false,
    playing: false,
    buffered: false,
    seekTime: -1,
    videoTime: 0,
    videoStartTime: 0,
    videoEndTime: 1,
    highlightStartTime: 0,
    highlightEndTime: 1,
    showTwitchUI: false,
};

const getters = {
    getReady: s => s.ready,
    getPlaying: s => s.playing,
    getBuffered: s => s.buffered,
    getSeekTime: s => s.seekTime,
    getVideoTime: s => s.videoTime,
    getVideoStartTime: s => s.videoStartTime,
    getVideoEndTime: s => s.videoEndTime,
    getHighlightStartTime: s => s.highlightStartTime,
    getHighlightEndTime: s => s.highlightEndTime,
    getShowTwitchUI: s => s.showTwitchUI,
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
    setVideoStartTime(s, videoStartTime) {
        s.videoStartTime = videoStartTime;
    },
    setVideoEndTime(s, videoEndTime) {
        s.videoEndTime = videoEndTime;
    },
    setHighlightStartTime(s, highlightStartTime) {
        s.highlightStartTime = highlightStartTime;
    },
    setHighlightEndTime(s, highlightEndTime) {
        s.highlightEndTime = highlightEndTime;
    },
    setShowTwitchUI(s, showTwitchUI) {
        s.showTwitchUI = showTwitchUI;
    },
};

const actions = {
    seekVideo({ commit }, newTime) {
        commit('setBuffered', false);
        commit('setSeekTime', newTime);
    },
};

export default {
    namespaced: true,
    state: localState,
    getters,
    mutations,
    actions,
};
