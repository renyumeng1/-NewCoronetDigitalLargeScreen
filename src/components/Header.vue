<template>
    <div>
        <header>
            <h1>中国疫情变化（{{StatisticalTime}}）</h1>
            <Time/>
        </header>
    </div>
</template>

<script>

import Time from "@/components/Time";
import axios from 'axios'

export default {
    // eslint-disable-next-line vue/multi-word-component-names
    name: "Header",
    components: {
        Time,
    },
    data() {
        return {
            StatisticalTime: ''
        }
    },
    mounted() {
        this.$bus.$on('getTime', time => {
            this.StatisticalTime = time
        })

    },
    beforeDestroy() {
        this.$bus.$off('getTime')
    }

}
</script>

<style scoped>
header {
    position: relative;
    height: 1.25rem;
    background: url(../assets/images/head_bg.png) no-repeat top center;
    background-size: 100% 100%;
}

header h1 {
    font-size: 0.475rem;
    color: #fff;
    text-align: center;
    line-height: 1rem;
}
</style>