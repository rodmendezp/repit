<template>
    <div>
        <b-button @click="startLabeling">Start Labeling</b-button>
    </div>
</template>

<script>
    import bButton from 'bootstrap-vue/es/components/button/button';

    export default {
        name: 'HomeView',
        components: {
            bButton,
        },
        methods: {
            startLabeling() {
                this.$router.push('/label/292622008/311/330');
            },
        },
    };
</script>

<style scoped>

</style>
