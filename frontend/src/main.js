// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue';
import Vuex from 'vuex';
import VueTouch from 'vue-touch';
import BootstrapVue from 'bootstrap-vue';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import 'bootstrap';
import App from './App';
import AppRouter from './router/app';
import store from './store';


Vue.use(Vuex);
Vue.use(BootstrapVue);
Vue.use(VueTouch, { name: 'v-touch' });
Vue.config.productionTip = false;

/* eslint-disable no-new */
new Vue({
    el: '#app',
    router: AppRouter,
    store,
    template: '<App/>',
    components: { App },
});
