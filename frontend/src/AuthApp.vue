<template>
    <div id="auth" class="container-fluid full-height" v-cloak>
        <router-view/>
    </div>
</template>

<script>
    export default {
        name: 'auth',
        data() {
            return {};
        },
        mounted() {

        },
    };
</script>

<style lang="sass">
    @import "~@/styles/landing/main.scss"
</style>
