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
            path: '/label/:video_id/:st_time/:end_time',
            name: 'LabelView',
            component: LabelView,
        },
    ],
});
