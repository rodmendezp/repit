<template>
    <div class="container-fluid full-height">
        <div class="row full-height align-items-center">
            <div class="col"></div>
            <div class="col">
                <h1>Welcome to Repit</h1>
                <b-button class="btn" @click="signIn">Sign In</b-button>
            </div>
            <div class="col"></div>
        </div>
    </div>
</template>

<script>
    import bButton from 'bootstrap-vue/es/components/button/button';

    export default {
        name: 'landing',
        data() {
            return {};
        },
        components: {
            bButton,
        },
        methods: {
            signIn() {
                location.href = 'http://127.0.0.1:8000/app/';
            },
        },
    };
</script>

<style lang="sass">
    @import "~@/styles/landing/main.scss"
</style>
