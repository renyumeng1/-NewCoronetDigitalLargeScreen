<template>
    <div class="panel bar" style="width: 100%;height: 3.875rem">
            <h2>
                昨日本土新增省市TOP10
            </h2>
            <div class="chart"></div>
            <div class="panel-footer"></div>
    </div>

</template>

<script>
import axios from 'axios'

export default {
    name: "PanelBar",
    data() {
        return {
            topCityName: '',
            topCityData: '',
            tempBar: true
        }
    },
    methods: {
        myChartBar(topCityName, topCityData) {
            // 实例化对象
            const myChart = this.$echart.init(document.querySelector(".bar .chart"));
            // 指定配置和数据
            let option = {
                color: ["#2f89cf"],
                tooltip: {
                    trigger: "axis",
                    axisPointer: {
                        // 坐标轴指示器，坐标轴触发有效
                        type: "shadow"
                    }
                },
                grid: {
                    left: "0%",
                    top: "10px",
                    right: "0%",
                    bottom: "4%",
                    containLabel: true
                },
                xAxis: [
                    {
                        type: "category",
                        //data: ["上海","云南","福建","广西","北京"],
                        data: topCityName,
                        axisTick: {
                            alignWithLabel: true
                        },
                        axisLabel: {
                            textStyle: {
                                color: "rgba(255,255,255,.6)",
                                fontSize: "12"
                            }
                        },
                        axisLine: {
                            show: false
                        }
                    }
                ],
                yAxis: [
                    {
                        type: "value",
                        axisLabel: {
                            textStyle: {
                                color: "rgba(255,255,255,.6)",
                                fontSize: "12"
                            }
                        },
                        axisLine: {
                            lineStyle: {
                                color: "rgba(255,255,255,.1)"
                                // width: 1,
                                // type: "solid"
                            }
                        },
                        splitLine: {
                            lineStyle: {
                                color: "rgba(255,255,255,.1)"
                            }
                        }
                    }
                ],
                series: [
                    {
                        name: "现有确诊",
                        type: "bar",
                        barWidth: "35%",
                        //data: [4579,1485,950,940,703],
                        data: topCityData,
                        itemStyle: {
                            barBorderRadius: 5
                        }
                    }
                ]
            };

            // 把配置给实例对象
            myChart.setOption(option);
            window.addEventListener("resize", function () {
                myChart.resize();
            });
        }
    },
    mounted() {
        axios
            .get('/api/top/')
            .then(response => {
                this.topCityName = response.data.topCityName
                this.topCityData = response.data.topCityData
                this.myChartBar(this.topCityName, this.topCityData)
                this.tempBar = false
            })
            .catch(error => {
                console.log(error)
            })
    },
    watch: {
        tempBar() {
            this.timer = setTimeout(() => {
                this.$bus.$emit('getBarTemp', this.tempBar)
            }, 2048)

        }
    },
    beforeDestroy() {
            //销毁定时器
            if (this.timer){
                clearInterval(this.timer)
            }
        }
}
</script>

<style scoped>

</style>