const localState = {
    keepLabeling: true,
    game: null,
    streamer: null,
    user: null,
};

const getters = {
    getKeepLabeling: s => s.keepLabeling,
    getGame: s => s.game,
    getStreamer: s => s.streamer,
    getUser: s => s.user,
};

const mutations = {
    setKeepLabeling(s, keepLabeling) {
        s.keepLabeling = keepLabeling;
    },
    setGame(s, game) {
        s.game = game;
    },
    setStreamer(s, streamer) {
        s.streamer = streamer;
    },
    setUser(s, user) {
        s.user = user;
    },
};

const actions = {};

export default {
    namespaced: true,
    state: localState,
    getters,
    mutations,
    actions,
};
