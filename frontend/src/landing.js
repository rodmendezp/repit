/* eslint-disable no-new */
import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import Landing from './LandingApp';

Vue.config.productionTip = false;
Vue.use(BootstrapVue);

new Vue({
    el: '#landing',
    template: '<Landing/>',
    components: { Landing },
});
