/* eslint-disable no-new */
import Vue from 'vue';
import Landing from './LandingApp';

Vue.config.productionTip = false;

new Vue({
    el: '#landing',
    template: '<Landing/>',
    components: { Landing },
});
