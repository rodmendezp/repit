/* eslint-disable no-new */
import Vue from 'vue';
import Vuex from 'vuex';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import Auth from './AuthApp';
import AuthRouter from './router/auth';
import store from './store';

Vue.use(Vuex);
Vue.config.productionTip = false;

new Vue({
    el: '#auth',
    router: AuthRouter,
    store,
    template: '<Auth/>',
    components: { Auth },
});
