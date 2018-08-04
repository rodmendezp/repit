<template>
    <div>
        Hello
        <b-button @click="appRepit">Sign In</b-button>
    </div>

</template>

<script>
    import bButton from 'bootstrap-vue/es/components/button/button';

    export default {
        name: 'landing',
        components: {
            bButton,
        },
        methods: {
            appRepit() {
                location.href = 'http://127.0.0.1:8000/accounts';
            },
        },
        mounted() {
            console.log('Landing mounted');
        },
    };
</script>

<style scoped>

</style>
