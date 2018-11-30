<template>
    <div>
        <button :disabled="isStartCursorLeft" class="btn-fa-style" @click="setExtraTimeZero(isStart)" v-if="isStart">
            <i class="fa fa-backward"></i>
        </button>
        <button :disabled="isMinusDisabled" class="btn-fa-style"
                @click="modifyTime(isStart, -1)" @mousedown="mouseDown(true)" @mouseup="mouseUp(true)">
            <i class="fa fa-minus"></i>
        </button>
        <button :disabled="isPlusDisabled" class="btn-fa-style"
                @click="modifyTime(isStart, 1)" @mousedown="mouseDown(false)" @mouseup="mouseUp(false)">
            <i class="fa fa-plus"></i>
        </button>
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
        data() {
            return {
                isMouseDown: [false, false],
            };
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
            mouseDown(isMinus) {
                if (this.isStart && isMinus) return;
                else if (!this.isStart && !isMinus) return;
                this.isMouseDown[isMinus ? 0 : 1] = true;
                setTimeout(() => this.setCursorCurrentTime(!isMinus), 500);
            },
            mouseUp(isMinus) {
                if (this.isMouseDown[isMinus ? 0 : 1]) this.isMouseDown[isMinus ? 0 : 1] = false;
            },
            setCursorCurrentTime(isStart) {
                if (this.isMouseDown[!isStart ? 0 : 1]) {
                    const time = isStart ? this.videoStartTime : this.videoEndTime;
                    this.modifyTime(isStart, this.videoTime - time);
                    if (this.isStart) setTimeout(() => this.setCursorCurrentTime(isStart), 500);
                }
            },
        },
        computed: {
            ...mapGetters({
                videoTime: 'player/getVideoTime',
                videoStartTime: 'player/getVideoStartTime',
                videoEndTime: 'player/getVideoEndTime',
                extraTimeLeft: 'player/getExtraTimeLeft',
                extraTimeRight: 'player/getExtraTimeRight',
            }),
            isMinusDisabled() {
                return (!this.isStart && this.isStartEqualEnd) || (this.isStart && this.isStartCursorLeft);
            },
            isPlusDisabled() {
                return (this.isStart && this.isStartEqualEnd) || (!this.isStart && this.isEndCursorRight);
            },
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
