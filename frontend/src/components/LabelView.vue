<template>
    <div>
        <twitch-player
            :videoId="$route.params.video_id"
            :stTime="$route.params.st_time"
            :endTime="$route.params.end_time"></twitch-player>
    </div>
</template>

<script>
    import TwitchPlayer from './player/TwitchPlayer';

    export default {
        name: 'LabelView',
        components: {
            TwitchPlayer,
        },
        data() {
            return {};
        },
    };
</script>

<style lang="sass">

</style>
