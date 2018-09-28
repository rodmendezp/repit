import Vue from 'vue';
import Router from 'vue-router';
import HomeView from '@/components/HomeView';
import LabelView from '@/components/LabelView';

Vue.use(Router);

export default new Router({
    routes: [
        {
            path: '/',
            name: 'HomeView',
            component: HomeView,
        },
        {
            path: '/label/',
            name: 'LabelView',
            component: LabelView,
        },
    ],
});
