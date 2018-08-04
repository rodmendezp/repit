import Vue from 'vue';
import Router from 'vue-router';
import SignInView from '@/components/auth/SignInView';

Vue.use(Router);


export default new Router({
    routes: [
        {
            path: '/',
            component: SignInView,
        },
    ],
});
