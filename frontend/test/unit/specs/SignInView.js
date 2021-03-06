import Vue from 'vue';
import SignIn from '@/components/auth/SignInView';

describe('SignIn.vue', () => {
    it('should render correct contents', () => {
        const Constructor = Vue.extend(SignIn);
        const vm = new Constructor().$mount();
        expect(vm.$el.querySelector('.hello h1').textContent).to.equal('Welcome to Your Vue.js App');
    });
});
