<template>
    <div>
        <dv-full-screen-container>
            <dv-loading v-if="showLoading">Loading...</dv-loading>
            <Header/>
            <AllCharts/>
        </dv-full-screen-container>

    </div>

</template>

<script>

import Header from "@/components/Header";
import AllCharts from "@/components/AllCharts";

export default {
    name: 'App',
    components: {
        AllCharts,
        Header,
    },
    data() {
        return {
            showLoading: true,
        }
    },
    methods:{
        getBarTemp(BarTemp){
            this.showLoading = BarTemp
        }
    },
    mounted() {
        this.$bus.$on('getBarTemp',this.getBarTemp)
    }
}
</script>

<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

li {
    list-style: none;
}

@font-face {
    font-family: electronicFont;
    src: url(./assets/font/DS-DIGIT.TTF);
}

body {
    font-family: Arial, Helvetica, sans-serif;
    margin: 0;
    padding: 0;
    /*  背景图定位 / 背景图尺寸  cover 完全铺满容器  contain 完整显示在容器内 */
    background: url(./assets/images/bg.jpg) no-repeat #000;
    background-size: cover;
    /* 行高是字体1.15倍 */
    line-height: 1.15;
}


.panel {
    position: relative;
    height: 3.875rem;
    border: 1px solid rgba(25, 186, 139, 0.17);
    background: rgba(255, 255, 255, 0.04) url(assets/images/line1.png);
    padding: 0 0.1875rem 0.5rem;
    margin-bottom: 0.1875rem;
}

.panel::before {
    position: absolute;
    top: 0;
    left: 0;
    content: "";
    width: 10px;
    height: 10px;
    border-top: 2px solid #02a6b5;
    border-left: 2px solid #02a6b5;
}

.panel::after {
    position: absolute;
    top: 0;
    right: 0;
    content: "";
    width: 10px;
    height: 10px;
    border-top: 2px solid #02a6b5;
    border-right: 2px solid #02a6b5;
}

.panel .panel-footer {
    position: absolute;
    left: 0;
    bottom: 0;
    width: 100%;
}

.panel .panel-footer::before {
    position: absolute;
    bottom: 0;
    left: 0;
    content: "";
    width: 10px;
    height: 10px;
    border-bottom: 2px solid #02a6b5;
    border-left: 2px solid #02a6b5;
}

.panel .panel-footer::after {
    position: absolute;
    bottom: 0;
    right: 0;
    content: "";
    width: 10px;
    height: 10px;
    border-bottom: 2px solid #02a6b5;
    border-right: 2px solid #02a6b5;
}

.panel h2 {
    height: 0.6rem;
    line-height: 0.6rem;
    text-align: center;
    color: #fff;
    font-size: 0.25rem;
    font-weight: 400;
}

.panel h2 a {
    margin: 0 0.1875rem;
    color: #fff;
    text-decoration: underline;
}

.panel .chart {
    height: 3rem;
}



@keyframes rotate {
    from {
        transform: translate(-50%, -50%) rotate(0deg);
    }
    to {
        transform: translate(-50%, -50%) rotate(360deg);
    }
}

@keyframes rotate1 {
    from {
        transform: translate(-50%, -50%) rotate(0deg);
    }
    to {
        transform: translate(-50%, -50%) rotate(-360deg);
    }
}

@media screen and (max-width: 1024px) {
    html {
        font-size: 42px !important;
    }
}

@media screen and (min-width: 1920) {
    html {
        font-size: 80px !important;
    }
}

</style>
