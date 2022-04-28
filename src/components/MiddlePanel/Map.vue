<template>
    <div class="map">
        <div class="chart"></div>
        <div class="map1"></div>
        <div class="map2"></div>
        <div class="map3"></div>
    </div>
</template>

<script>
import '../../assets/js/china'
import axios from 'axios'

export default {
    name: "Map",
    data(){
        return {
            mapData:'',
            provinceName:''
        }
    },
    methods: {
        myChartMap(mapData) {
            // 1. 实例化对象
            const myChart = this.$echart.init(document.querySelector(".map .chart"));
            let option = {
                title: {
                    text: "中国疫情分布图（累计）",
                    left: 350, //设置标题的距离盒子左边的距离
                    top: 100, //设置标题距离盒子顶部的距离
                    color:'#a61919'
                },

                series: [
                    {
                        name: "确诊人数", //控制鼠标hover上去显示的固定文本
                        type: "map", //告诉echarts需要渲染一个地图
                        mapType: "china", //告诉echarts要渲染注册的china地图
                        label: {
                            show: true, //控制是否显示省份的名称
                            color: "white" // 设置显示每个省份的字体颜色
                        },
                        itemStyle: {
                            borderColor: "green" //每个省份的边界的颜色
                        },
                        emphasis: { //控制鼠标移入的版块的颜色
                            color: "#fff", //移入该模块的字体颜色
                            itemStyle: {
                                areaColor: "#83b5e7", //鼠标hover到模块上的背景色
                            }
                        },
                        zoom: 1.2, //控制整个地图的缩放倍数
                        data: mapData //TODO 每个板块的数据TODO
                    }
                ],
                visualMap: [{
                    type: "piecewise", //左下角的分段显示
                    show: true,
                    splitNumber: 4, //显示几个分段
                    pieces: [ //左下角的自定义分段显示
                        {min: 15000},
                        {min: 900, max: 15000},
                        {min: 310, max: 900},
                        {min: 200, max: 310},
                        {min: 0, max: 200}],

                    align: "right",
                    left: 0,
                    top: 550,
                    inRange: {
                        symbol: "circle",
                        color: ["#ffc0b1", "#9c0505"]
                    }
                }],
                tooltip: {
                    trigger: "item",
                    formatter: function (params) {
                        return params.name + "<br/>" + params.seriesName + "：" + params.value
                    }
                },
            }
            myChart.setOption(option)
            myChart.on('click',params =>{
                this.provinceName = params.data.name
                this.$bus.$emit('sendProvinceName',this.provinceName)
            })
            window.addEventListener("resize", function () {
                myChart.resize();
            });
        }
    },
    mounted() {
        axios
            .get('/api/right/map/')
            .then(response => {
                this.mapData = response.data.mapData
                this.myChartMap(this.mapData)
            })
    }
}
</script>

<style scoped>
.map {
    position: relative;
    height: 10.125rem;
}

.map .chart {
    position: absolute;
    top: 0;
    left: 0;
    z-index: 5;
    height: 10.125rem;
    width: 100%;
}

.map .map1,
.map .map2,
.map .map3 {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 6.475rem;
    height: 6.475rem;
    background: url(../../assets/images/map.png) no-repeat;
    background-size: 100% 100%;
    opacity: 0.3;
}

.map .map2 {
    width: 8.0375rem;
    height: 8.0375rem;
    background-image: url(../../assets/images/lbx.png);
    opacity: 0.6;
    animation: rotate 15s linear infinite;
    z-index: 2;
}

.map .map3 {
    width: 7.075rem;
    height: 7.075rem;
    background-image: url(../../assets/images/jt.png);
    animation: rotate1 10s linear infinite;
}
</style>