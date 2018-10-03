<template>
    <div class="seek-bar-container">
        <div>
            <div class="progress-bar-container">
                <div class="candidate-bar" :style="`margin-left: ${candidateBarLeft}; width: ${candidateBarWidth}`"></div>
                <div class="progress-bar"></div>
            </div>
            <div class="thumb-container" ref="thumbContainer"
                 @mousemove="mouseMoveContainer"
                 @mouseover="mouseOverContainer"
                 @mouseleave="mouseLeaveContainer"
                 @mousedown="mouseDownContainer">
                <div class="thumb" :style="{left: thumbLeftPercentage}"></div>
            </div>
        </div>
    </div>
</template>

<script>
    import { mapGetters, mapActions } from 'vuex';

    export default {
        name: 'VideoSeekBar',
        data() {
            return {
                mouseOver: false,
                mouseDown: false,
                mouseTime: 0,
                inputTime: 0,
            };
        },
        computed: {
            ...mapGetters({
                videoTime: 'player/getVideoTime',
                videoStartTime: 'player/getVideoStartTime',
                videoEndTime: 'player/getVideoEndTime',
                extraTimeRight: 'player/getExtraTimeRight',
                extraTimeLeft: 'player/getExtraTimeLeft',
                videoInfo: 'twitchdata/getVideoInfo',
            }),
            thumbLeftPercentage() {
                let percent = 0;
                if (this.mouseDown) {
                    percent = (100 * (this.mouseTime - (this.videoStartTime - this.extraTimeLeft))) / this.totalTime;
                } else percent = (100 * (this.inputTime - (this.videoStartTime - this.extraTimeLeft))) / this.totalTime;
                return `${percent}%`;
            },
            totalTime() {
                return (this.videoEndTime - this.videoStartTime) + (this.extraTimeLeft + this.extraTimeRight);
            },
            candidateBarLeft() {
                return `${100 * ((this.extraTimeLeft) / this.totalTime)}%`;
            },
            candidateBarWidth() {
                return `${100 * ((this.videoEndTime - this.videoStartTime) / this.totalTime)}%`;
            },
        },
        methods: {
            mouseMoveContainer(e) {
                if (document.selection) document.selection.empty();
                else window.getSelection().removeAllRanges();
                let x = e.target === this.$refs.thumbContainer ? e.offsetX :
                    e.pageX - this.$refs.thumbContainer.getBoundingClientRect().left;
                const minOffset = 0;
                const maxOffset = this.$refs.thumbContainer.clientWidth;
                const stOffset = maxOffset * (this.extraTimeLeft / this.totalTime);
                const endOffset = maxOffset * ((this.totalTime - this.extraTimeRight) / this.totalTime);
                x = x >= stOffset ? x : stOffset;
                x = x > endOffset ? endOffset : x;
                this.mouseTime = ((x) / (maxOffset - minOffset)) * this.totalTime;
                this.mouseTime += this.videoStartTime - this.extraTimeLeft;
                if (this.pressed) this.inputTime = this.mouseTime;
            },
            mouseOverContainer() {
                this.mouseOver = true;
            },
            mouseLeaveContainer() {
                this.mouseOver = false;
            },
            mouseDownContainer(e) {
                this.mouseDown = true;
                document.documentElement.addEventListener('mouseup', this.mouseUp);
                document.documentElement.addEventListener('mousemove', this.mouseMoveContainer);
                this.mouseMoveContainer(e);
            },
            mouseUp() {
                this.mouseDown = false;
                this.seekVideo(this.mouseTime);
                document.documentElement.removeEventListener('mouseup', this.mouseUp);
                document.documentElement.removeEventListener('mousemove', this.mouseMoveContainer);
            },
            ...mapActions({
                seekVideo: 'player/seekVideo',
            }),
        },
        mounted() {},
        watch: {
            videoTime() {
                if (!this.mouseDown) this.inputTime = this.videoTime;
            },
        },
    };
</script>

<style lang="sass">
    $thumb-height: 19px
    $thumb-width: 12px

    .seek-bar-container
        padding-left: 10px
        padding-right: 10px
        width: 100%
        background: transparent
        height: 30px
        z-index: 2
        > div
            width: 100%
            padding-left: 0
            padding-right: 0
            position: relative
            height: inherit
            z-index: inherit
            > div
                z-index: inherit
                > div
                    z-index: inherit

    .progress-bar-container
        height: 6px
        position: absolute
        margin-top: 11px
        width: 100%
        padding-right: 2px
        background: transparent
        z-index: 2

        .progress-bar
            background: rgba(255,255,255,0.3)
            width: 100%
            height: 6px
            
        .candidate-bar
            background: #ffb300
            height: 6px
            position: absolute

    .thumb-container
        height: $thumb-height
        margin-top: 11px - ($thumb-height - 6px) / 2
        position: absolute
        width: 100%
        padding-right: $thumb-width / 2
        background: transparent
        cursor: pointer

        > div
            position: relative

        .thumb
            pointer-events: none
            position: absolute
            margin-left: 0
            width: $thumb-width
            height: $thumb-height
            background: #0397e2
            float: left
            border-radius: 20%
            border: 1px solid rgba(56, 51, 57, 0.74)
            box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2)
</style>
