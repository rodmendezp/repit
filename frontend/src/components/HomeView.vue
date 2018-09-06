<template>
    <div class="row full-height align-items-center">
        <div class="col"></div>
        <div style="text-align: center" class="col">
            <h1 v-if="user"> Welcome {{ user.first_name }}</h1>
            <button class="btn btn-primary" @click="startLabeling">Start Labeling</button>
        </div>
        <div class="col"></div>
    </div>
</template>

<script>
    import { mapGetters } from 'vuex';

    export default {
        name: 'HomeView',
        methods: {
            startLabeling() {
                this.$router.push('/label/305043183/311/330');
            },
        },
        computed: {
            ...mapGetters({
                user: 'getUser',
            }),
        },
        mounted() {
        },
    };
</script>

<style>

</style>
