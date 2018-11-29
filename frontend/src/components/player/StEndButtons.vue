<template>
    <div>
        <button :disabled="isStartCursorLeft" class="btn-fa-style" @click="setExtraTimeZero(isStart)" v-if="isStart">
            <i class="fa fa-backward"></i>
        </button>
        <button :disabled="(!isStart && isStartEqualEnd) || (isStart && isStartCursorLeft)"
                class="btn-fa-style" @click="modifyTime(isStart, -1)"><i class="fa fa-minus"></i></button>
        <button :disabled="(isStart && isStartEqualEnd) || (!isStart && isEndCursorRight)"
                class="btn-fa-style" @click="modifyTime(isStart, 1)"><i class="fa fa-plus"></i></button>
        <button :disabled="isEndCursorRight" class="btn-fa-style" @click="setExtraTimeZero(isStart)" v-if="!isStart">
            <i class="fa fa-forward"></i>
        </button>
    </div>
</template>

<script>
    import { mapGetters, mapMutations } from 'vuex';

    export default {
        name: 'StEndButtons',
        props: {
            time: { type: Number },
            isStart: { type: Boolean },
        },
        methods: {
            ...mapMutations({
                setVideoStartTime: 'player/setVideoStartTime',
                setVideoEndTime: 'player/setVideoEndTime',
                setExtraTimeLeft: 'player/setExtraTimeLeft',
                setExtraTimeRight: 'player/setExtraTimeRight',
            }),
            setExtraTimeZero(isStart) {
                if (isStart) {
                    this.setVideoStartTime(this.videoStartTime - this.extraTimeLeft);
                    this.setExtraTimeLeft(0);
                } else {
                    this.setVideoEndTime(this.videoEndTime + this.extraTimeRight);
                    this.setExtraTimeRight(0);
                }
            },
            modifyTime(isStart, deltaSeconds) {
                const time = isStart ? this.videoStartTime : this.videoEndTime;
                const newTime = time + deltaSeconds;
                const extraTime = isStart ? this.extraTimeLeft : this.extraTimeRight;
                const timeLimit = isStart ? time - extraTime : time + extraTime;
                const outsideLimit = isStart ? newTime < timeLimit : newTime > timeLimit;
                const surpassTime = isStart ? newTime >= this.videoEndTime : newTime <= this.videoStartTime;
                const modifyTimeFunc = isStart ? this.setVideoStartTime : this.setVideoEndTime;
                const modifyExtraFunc = isStart ? this.setExtraTimeLeft : this.setExtraTimeRight;
                if (outsideLimit) {
                    modifyTimeFunc(time + extraTime);
                    modifyExtraFunc(0);
                } else if (surpassTime) {
                    modifyTimeFunc(isStart ? this.videoEndTime : this.videoStartTime);
                    modifyExtraFunc(isStart ? this.videoEndTime - timeLimit : timeLimit - this.videoStartTime);
                } else {
                    modifyTimeFunc(newTime);
                    modifyExtraFunc(extraTime + ((isStart ? 1 : -1) * deltaSeconds));
                }
            },
        },
        computed: {
            ...mapGetters({
                videoStartTime: 'player/getVideoStartTime',
                videoEndTime: 'player/getVideoEndTime',
                extraTimeLeft: 'player/getExtraTimeLeft',
                extraTimeRight: 'player/getExtraTimeRight',
            }),
            isStartCursorLeft() {
                return this.extraTimeLeft === 0;
            },
            isStartEqualEnd() {
                return this.videoStartTime === this.videoEndTime;
            },
            isEndCursorRight() {
                return this.extraTimeRight === 0;
            },
        },
    };
</script>

<style lang="sass">

</style>
