<template>
    <div class="panel line">
        <h2>近十日中国新增趋势</h2>
        <div class="chart"></div>
        <div class="panel-footer"></div>
    </div>
</template>

<script>
// import $ from 'jquery'
import axios from 'axios'

export default {
    name: "PanelLine",
    data() {
        return {
            confirms: '',
            dates: '',
            deads: '',
            heals: '',
            storeConfirms: '',
        }
    },
    methods: {
        myChartLine(storeConfirms, confirms, deads, heals, dates) {
            // 基于准备好的dom，初始化eCharts实例
            const myChart = this.$echart.init(document.querySelector(".line .chart"));

            // (1)准备数据
            let data = {
                peopleNum: [
                    storeConfirms,
                    confirms,
                    deads,
                    heals
                ]
            };


            let option = {
                color: ["#00f2f1", "#ed3f35", "red", "blue"],
                tooltip: {
                    // 通过坐标轴来触发
                    trigger: "axis"
                },
                legend: {
                    // 距离容器10%
                    right: "10%",
                    // 修饰图例文字的颜色
                    textStyle: {
                        color: "#4c9bfd"
                    }
                    // 如果series 里面设置了name，此时图例组件的data可以省略

                },
                grid: {
                    top: "20%",
                    left: "3%",
                    right: "4%",
                    bottom: "3%",
                    show: true,
                    borderColor: "#012f4a",
                    containLabel: true
                },

                xAxis: {
                    type: "category",
                    boundaryGap: false,
                    data: dates,
                    // 去除刻度
                    axisTick: {
                        show: false
                    },
                    // 修饰刻度标签的颜色
                    axisLabel: {
                        color: "rgba(255,255,255,.7)"
                    },
                    // 去除x坐标轴的颜色
                    axisLine: {
                        show: false
                    }
                },
                yAxis: {
                    type: "value",
                    // 去除刻度
                    axisTick: {
                        show: false
                    },
                    // 修饰刻度标签的颜色
                    axisLabel: {
                        color: "rgba(255,255,255,.7)"
                    },
                    // 修改y轴分割线的颜色
                    splitLine: {
                        lineStyle: {
                            color: "#012f4a"
                        }
                    }
                },
                series: [
                    {
                        name: "无症状",
                        type: "line",
                        stack: "总量",
                        // 是否让线条圆滑显示
                        smooth: true,
                        data: data.peopleNum[0]
                    },
                    {
                        name: "确诊",
                        type: "line",
                        stack: "总量",
                        smooth: true,
                        data: data.peopleNum[1]
                    },
                    {
                        name: "死亡",
                        type: "line",
                        stack: "总量",
                        smooth: true,
                        data: data.peopleNum[2]
                    },
                    {
                        name: "治愈",
                        type: "line",
                        stack: "总量",
                        smooth: true,
                        data: data.peopleNum[3]
                    }
                ]
            };
            // 3. 把配置和数据给实例对象
            myChart.setOption(option);

            // 重新把配置好的新数据给实例对象
            myChart.setOption(option);
            window.addEventListener("resize", function () {
                myChart.resize();
            });
        },
        getAllData() {
            axios
                .get('/api/left/line/')
                .then(response => {
                    this.confirms = response.data.confirms
                    this.dates = response.data.dates
                    this.deads = response.data.deads
                    this.heals = response.data.heals
                    this.storeConfirms = response.data.storeConfirms
                    console.log(this.confirms)
                    console.log(this.heals)
                    this.myChartLine(this.storeConfirms, this.confirms, this.deads, this.heals, this.dates)
                })
                .catch(error => {
                    console.log(error)
                })
        }
    },
    mounted() {
        this.getAllData()
    }
}
</script>

<style scoped>

</style>