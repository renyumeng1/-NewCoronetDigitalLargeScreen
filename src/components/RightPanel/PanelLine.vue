<template>
    <div class="panel line1">
        <h2>test</h2>
        <div class="chart"></div>
        <div class="panel-footer"></div>
    </div>
</template>

<script>
export default {
    name: "PanelLine",
    data() {
        return {
            confirms: '',
            deads: '',
            dates:''
        }
    },
    methods: {
        myChartLine(confirms, deads,dates) {
            const myChart = this.$echart.init(document.querySelector(".line1 .chart"));

            let option = {
                tooltip: {
                    trigger: "axis",
                    axisPointer: {
                        lineStyle: {
                            color: "#dddc6b"
                        }
                    }
                },
                legend: {
                    top: "0%",
                    textStyle: {
                        color: "rgba(255,255,255,.5)",
                        fontSize: "12"
                    }
                },
                grid: {
                    left: "10",
                    top: "30",
                    right: "10",
                    bottom: "10",
                    containLabel: true
                },

                xAxis: [
                    {
                        type: "category",
                        boundaryGap: false,
                        axisLabel: {
                            textStyle: {
                                color: "rgba(255,255,255,.6)",
                                fontSize: 12
                            }
                        },
                        axisLine: {
                            lineStyle: {
                                color: "rgba(255,255,255,.2)"
                            }
                        },

                        data: dates
                    },
                    {
                        axisPointer: {show: false},
                        axisLine: {show: false},
                        position: "bottom",
                        offset: 20
                    }
                ],

                yAxis: [
                    {
                        type: "value",
                        axisTick: {show: false},
                        axisLine: {
                            lineStyle: {
                                color: "rgba(255,255,255,.1)"
                            }
                        },
                        axisLabel: {
                            textStyle: {
                                color: "rgba(255,255,255,.6)",
                                fontSize: 12
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
                        name: "累计已治愈",
                        type: "line",
                        smooth: true,
                        symbol: "circle",
                        symbolSize: 5,
                        showSymbol: false,
                        lineStyle: {
                            normal: {
                                color: "#0184d5",
                                width: 2
                            }
                        },
                        areaStyle: {
                            normal: {
                                color: new this.$echart.graphic.LinearGradient(
                                    0,
                                    0,
                                    0,
                                    1,
                                    [
                                        {
                                            offset: 0,
                                            color: "rgba(1, 132, 213, 0.4)"
                                        },
                                        {
                                            offset: 0.8,
                                            color: "rgba(1, 132, 213, 0.1)"
                                        }
                                    ],
                                    false
                                ),
                                shadowColor: "rgba(0, 0, 0, 0.1)"
                            }
                        },
                        itemStyle: {
                            normal: {
                                color: "#0184d5",
                                borderColor: "rgba(221, 220, 107, .1)",
                                borderWidth: 12
                            }
                        },
                        data: confirms
                    },
                    {
                        name: "累计死亡",
                        type: "line",
                        smooth: true,
                        symbol: "circle",
                        symbolSize: 5,
                        showSymbol: false,
                        lineStyle: {
                            normal: {
                                color: "#00d887",
                                width: 2
                            }
                        },
                        areaStyle: {
                            normal: {
                                color: new this.$echart.graphic.LinearGradient(
                                    0,
                                    0,
                                    0,
                                    1,
                                    [
                                        {
                                            offset: 0,
                                            color: "rgba(0, 216, 135, 0.4)"
                                        },
                                        {
                                            offset: 0.8,
                                            color: "rgba(0, 216, 135, 0.1)"
                                        }
                                    ],
                                    false
                                ),
                                shadowColor: "rgba(0, 0, 0, 0.1)"
                            }
                        },
                        itemStyle: {
                            normal: {
                                color: "#00d887",
                                borderColor: "rgba(221, 220, 107, .1)",
                                borderWidth: 12
                            }
                        },
                        data: deads
                    }
                ]
            };

            // 使用刚指定的配置项和数据显示图表。
            myChart.setOption(option);
            window.addEventListener("resize", function () {
                myChart.resize();
            });
        }
    },
    mounted() {
        this.$bus.$on('sendDataToRightLine', (dataAll) => {
            this.confirms = dataAll.confirms
            this.deads = dataAll.deads
            this.dates = dataAll.dates
            console.log(this.confirms)
            this.myChartLine(this.confirms, this.deads,this.dates)
        })

    }
}
</script>

<style scoped>

</style>