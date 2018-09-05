<template>
    <div id="app" class="container-fluid full-height" v-cloak>
        <router-view/>
    </div>
</template>

<script>
    import { mapMutations } from 'vuex';

    export default {
        name: 'App',
        methods: {
            ...mapMutations({
                setUser: 'setUser',
            }),
        },
        mounted() {
            /* eslint no-undef: 0 */
            const userSplit = LOGGED_USER.value.split(';');
            if (userSplit.length === 3) {
                this.setUser({
                    first_name: userSplit[0],
                    last_name: userSplit[1],
                    email: userSplit[2],
                });
            } else {
                console.log('Somehting went wrong, maybe user not logged?');
                console.log('LOGGED_USER.value = ', LOGGED_USER.value);
            }
        },
    };
</script>

<style lang="sass">
    @import "~@/styles/app/main.scss"
</style>
