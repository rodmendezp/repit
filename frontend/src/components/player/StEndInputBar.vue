<template>
    <div class="st-end-input-container">
        <div>
            <div class="st-end-input-bar-container">
                <div class="st-end-input-bar"></div>
            </div>
            <div class="st-end-thumb-container" ref="stEndThumbContainer"
                 @mousemove="mouseMoveBar"
                 @mouseover="mouseOverBar"
                 @mouseleave="mouseLeaveBar">
                <div class="thumb-st" :style="{left: stThumbLeft}" @mousedown="mouseDownStThumb"></div>
                <div class="thumb-end" :style="{left: endThumbLeft}" @mousedown="mouseDownEndThumb"></div>
                <div class="time-container" :style="{left: stThumbLeft}">
                    <div class="time">
                        <span v-if="mouseDownSt">{{ mouseTimeString }}</span>
                        <span v-else>{{ videoStartTimeString }}</span>
                    </div>
                </div>
                <div class="time-container" :style="{left: endThumbLeft}">
                    <div class="time">
                        <span v-if="mouseDownEnd">{{ mouseTimeString }}</span>
                        <span v-else>{{ videoEndTimeString }}</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import moment from 'moment';
    import { mapGetters, mapMutations } from 'vuex';

    export default {
        name: 'StEndInputBar',
        data() {
            return {
                defaultExtraTime: 15,
                mouseDownSt: false,
                mouseDownEnd: false,
                mouseTime: 0,
                mouseOver: false,
            };
        },
        computed: {
            ...mapGetters({
                videoTime: 'player/getVideoTime',
                videoStartTime: 'player/getVideoStartTime',
                videoEndTime: 'player/getVideoEndTime',
                videoLength: 'player/getVideoLength',
                extraTimeLeft: 'player/getExtraTimeLeft',
                extraTimeRight: 'player/getExtraTimeRight',
            }),
            barTotalTime() {
                return (this.extraTimeLeft + this.extraTimeRight) + (this.videoEndTime - this.videoStartTime);
            },
            stThumbLeft() {
                let percent = 0;
                if (this.mouseDownSt) {
                    percent = 100 * ((this.mouseTime - (this.videoStartTime - this.extraTimeLeft)) / this.barTotalTime);
                } else percent = 100 * (this.extraTimeLeft / this.barTotalTime);
                return `${percent}%`;
            },
            endThumbLeft() {
                let percent = 0;
                if (this.mouseDownEnd) {
                    percent = 100 * ((this.mouseTime - (this.videoStartTime - this.extraTimeLeft)) / this.barTotalTime);
                } else percent = 100 * ((this.barTotalTime - this.extraTimeRight) / this.barTotalTime);
                return `${percent}%`;
            },
            mouseTimeString() {
                return `${moment(0).startOf('day').second(this.mouseTime).format('H:mm:ss')}`;
            },
            videoStartTimeString() {
                return `${moment(0).startOf('day').second(this.videoStartTime).format('H:mm:ss')}`;
            },
            videoEndTimeString() {
                return `${moment(0).startOf('day').second(this.videoEndTime).format('H:mm:ss')}`;
            },
        },
        mounted() {
            this.updateExtraTimes();
        },
        methods: {
            ...mapMutations({
                setExtraTimeLeft: 'player/setExtraTimeLeft',
                setExtraTimeRight: 'player/setExtraTimeRight',
                setVideoStartTime: 'player/setVideoStartTime',
                setVideoEndTime: 'player/setVideoEndTime',
            }),
            addEventsMouseDown() {
                document.documentElement.addEventListener('mouseup', this.mouseUp);
                document.documentElement.addEventListener('mousemove', this.mouseMoveBar);
            },
            mouseMoveBar(e) {
                if (document.selection) document.selection.empty();
                else window.getSelection().removeAllRanges();
                let x = e.target === this.$refs.stEndThumbContainer ?
                    e.offsetX : e.pageX - this.$refs.stEndThumbContainer.getBoundingClientRect().left;
                const minOffset = 0;
                const maxOffset = this.$refs.stEndThumbContainer.clientWidth;
                const stOffset = (maxOffset * (this.extraTimeLeft / this.barTotalTime)) + 12;
                const endOffset = (maxOffset * ((this.barTotalTime - this.extraTimeRight) / this.barTotalTime)) - 12;
                if (this.mouseDownEnd) {
                    x = x >= stOffset ? x : stOffset;
                } else x = x >= minOffset ? x : minOffset;
                if (this.mouseDownSt) {
                    x = x > endOffset ? endOffset : x;
                } else x = x > maxOffset ? maxOffset : x;
                this.mouseTime = ((x) / (maxOffset - minOffset)) * this.barTotalTime;
                this.mouseTime += (this.videoStartTime - this.extraTimeLeft);
            },
            mouseOverBar() {
                this.mouseOver = true;
            },
            mouseLeaveBar() {
                this.mouseOver = false;
            },
            mouseDownStThumb(e) {
                this.mouseDownSt = true;
                this.addEventsMouseDown();
                this.mouseMoveBar(e);
            },
            mouseDownEndThumb(e) {
                this.mouseDownEnd = true;
                this.addEventsMouseDown();
                this.mouseMoveBar(e);
            },
            mouseUp() {
                document.documentElement.removeEventListener('mouseup', this.mouseUp);
                document.documentElement.removeEventListener('mousemove', this.mouseMoveBar);
                if (this.mouseDownSt) {
                    const minTime = this.videoStartTime - this.extraTimeLeft;
                    this.setVideoStartTime(this.mouseTime);
                    this.setExtraTimeLeft(this.videoStartTime - minTime);
                    this.mouseDownSt = false;
                }
                if (this.mouseDownEnd) {
                    const maxTime = this.videoEndTime + this.extraTimeRight;
                    this.setVideoEndTime(this.mouseTime);
                    this.setExtraTimeRight(maxTime - this.videoEndTime);
                    this.mouseDownEnd = false;
                }
            },
            updateExtraTimes() {
                if (this.videoEndTime + this.defaultExtraTime > this.videoLength) {
                    this.setExtraTimeRight(this.videoLength - this.videoEndTime);
                } else this.setExtraTimeRight(this.defaultExtraTime);
                if (this.videoStartTime < this.defaultExtraTime) this.setExtraTimeLeft(this.videoStartTime);
                else this.setExtraTimeLeft(this.defaultExtraTime);
            },
        },
        watch: {
            videoLength() {
                this.updateExtraTimes();
            },
        },
    };
</script>

<style scoped lang="sass">
    $thumb-height: 19px
    $thumb-width: 12px

    .st-end-input-container
        height: 30px
        width: 100%
        background: transparent
        padding-left: 10px
        padding-right: 10px
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

    .st-end-input-bar-container
        height: 6px
        position: absolute
        margin-top: 16px
        width: 100%
        padding-right: 2px
        background: transparent
        z-index: 2

        .st-end-input-bar
            background: rgba(255, 255, 255, 0.3)
            height: 6px
            width: 100%

    .st-end-thumb-container
        height: $thumb-height
        margin-top: 16px - ($thumb-height - 6px) / 2
        position: absolute
        width: 100%
        padding-right: $thumb-width / 2
        background: transparent

        > div
            position: relative

        .thumb-st, .thumb-end
            cursor: pointer
            position: absolute
            margin-left: -6px
            width: $thumb-width
            height: $thumb-height
            background: #ffb300
            float: left
            border-radius: 20%
            border: 1px solid rgba(56, 51, 57, 0.74)
            box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2)

        .time-container
            position: absolute
            width: 0
            z-index: 0

        .time
            position: relative
            top: -18px
            left: -24px
            font-size: 12px
            color: white
            span
                z-index: 3
                background: #111
                padding: 1px 5px
                border-radius: 3px

</style>
