<template>
    <div>
        <button @click=""></button>
        <button @mousedown=""></button>
        <button @click=""></button>
    </div>
</template>

<script>
    export default {
        name: 'StEndButtons',
        props: {
            time: { type: Number },
            isStart: { },
        },
        mounted() {
            console.log(this.time);
            console.log(this.isStart);
        },
        watch: {
            time(oldVal, newVal) {
                console.log('oldVal = ', oldVal);
                console.log('newVal = ', newVal);
            },
        },
    };
</script>

<style scoped>

</style>
