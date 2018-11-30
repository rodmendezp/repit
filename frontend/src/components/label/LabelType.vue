<template>
    <div class="container">
        <div class="row form-group">
            <div class="offset-sm-1 col-sm-2 repit-text">Type</div>
            <div class="" v-if="!typeSetted">Choose a type from the options below</div>
            <button class="btn type-btn-active btn-primary" v-if="typeSetted">{{ highlight.type }}</button>
            <button class="btn type-btn-hidden btn-primary" v-else>H</button>
        </div>
        <div class="row form-group">
            <div class="col-sm-3 repit-text" v-if="!typeSetted"></div>
            <div class="col-sm-3 repit-text" v-else>Click to change</div>
            <button :class="`btn type-btn ${getTypeBtnMargin(index)}`" v-for="(hlType, index) in hlTypes"
                    @click="typeSelected(hlType)" v-if="hlType !== highlight.type">{{ hlType }}</button>
        </div>
    </div>
</template>

<script>
    import { mapGetters, mapMutations } from 'vuex';

    export default {
        name: 'LabelType',
        data() {
            return {
                typeSetted: false,
            };
        },
        methods: {
            typeSelected(hlType) {
                this.$emit('type-setted');
                this.typeSetted = false;
                this.typeSetted = true;
                this.setHighlightType(hlType);
            },
            getTypeBtnMargin(index) {
                if (index === null || index === undefined) {
                    return '';
                } else if (this.typeSetted && index === 1 && this.highlight.type === this.hlTypes[0]) {
                    return 'type-btn-margin-st';
                } else if (index === 0) {
                    return 'type-btn-margin-st';
                }
                return 'type-btn-margin';
            },
            ...mapMutations({
                setHighlightType: 'highlight/setHighlightType',
            }),
        },
        computed: {
            ...mapGetters({
                hlTypes: 'highlight/getTypes',
                highlight: 'highlight/getHighlight',
            }),
        },
    };
</script>

<style scoped lang="sass">
    .type-btn, .type-btn-active, .type-btn-hidden
        padding: 1px 6px !important

    .type-btn-hidden
        visibility: hidden

    .type-btn-margin
        margin-left: 5px
        margin-right: 5px

    .type-btn-margin-st
        margin-right: 5px

    .repit-text
        color: white
</style>
