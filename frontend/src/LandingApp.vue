<template>
    <div class="main-container full-height">
        <div class="welcome-container">
            <h1>Welcome to Repit</h1>
            <button class="btn btn-primary btn-lg" @click="signIn">Sign In</button>
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
                window.location.replace('/app');
            },
        },
    };
</script>

<style lang="sass">
    @import "~@/styles/landing/main.scss"

    .main-container
        display: flex
        flex-direction: column
        justify-content: center

    .welcome-container
        display: flex
        flex-direction: column
        justify-content: space-evenly
        align-items: center
        height: 20%

    .welcome-container > h1
        font-size: 4vh

    .welcome-container > button
        font-size: 2.5vh

</style>
