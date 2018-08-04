/* eslint-disable no-new */
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import Vue from 'vue';
import Auth from './AuthApp';
import AuthRouter from './router/auth';

Vue.config.productionTip = false;

new Vue({
    el: '#auth',
    router: AuthRouter,
    template: '<Auth/>',
    components: { Auth },
});
