import Vue from 'vue';
import Router from 'vue-router';
import SignInView from '@/components/auth/SignInView';
import SignUpView from '@/components/auth/SignUpView';

Vue.use(Router);

export default new Router({
    routes: [
        {
            path: '/',
            component: SignInView,
        },
        {
            path: '/signup',
            component: SignUpView,
        },
    ],
});
