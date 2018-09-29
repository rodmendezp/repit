const localState = {
    keepLabeling: true,
};

const getters = {
    getKeepLabeling: s => s.keepLabeling,
};

const mutations = {
    setKeepLabeling(s, keepLabeling) {
        s.keepLabeling = keepLabeling;
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
