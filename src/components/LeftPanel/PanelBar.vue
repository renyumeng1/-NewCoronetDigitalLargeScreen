<template>
    <div class="panel bar">
        <h2>
            柱状图-就业行业 <a href="#">2019</a>
            <a href="#"> 2020</a>
        </h2>
        <div class="chart"></div>
        <div class="panel-footer"></div>
    </div>
</template>

<script>
    import $ from 'jquery'
    export default {
        name: "PanelBar",
        methods:{
            myChartBar() {
                // 实例化对象
                const myChart = this.$echart.init(document.querySelector(".bar .chart"));
                // 指定配置和数据
                let option = {
                    color: ["#2f89cf"],
                    tooltip: {
                        trigger: "axis",
                        axisPointer: {
                            // 坐标轴指示器，坐标轴触发有效
                            type: "shadow" // 默认为直线，可选为：'line' | 'shadow'
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
                            data: [
                                "旅游行业",
                                "教育培训",
                                "游戏行业",
                                "医疗行业",
                                "电商行业",
                                "社交行业",
                                "金融行业"
                            ],
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
                            name: "直接访问",
                            type: "bar",
                            barWidth: "35%",
                            data: [200, 300, 300, 900, 1500, 1200, 600],
                            itemStyle: {
                                barBorderRadius: 5
                            }
                        }
                    ]
                };

                // 把配置给实例对象
                myChart.setOption(option);
                window.addEventListener("resize", function() {
                    myChart.resize();
                });
                // 数据变化
                let dataAll = [
                    { year: "2019", data: [200, 300, 300, 900, 1500, 1200, 600] },
                    { year: "2020", data: [300, 400, 350, 800, 1800, 1400, 700] }
                ];

                $(".bar h2 ").on("click", "a", function() {
                    option.series[0].data = dataAll[$(this).index()].data;
                    myChart.setOption(option);
                });
            }
        },
        mounted() {
            this.myChartBar()
        }
    }
</script>

<style scoped>

</style>