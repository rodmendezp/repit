<template>
    <div>
        Video_ID: {{ $route.params.video_id }}
        St_Time: {{ $route.params.st_time }}
        End_Time: {{ $route.params.end_time }}
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

<style>

</style>
