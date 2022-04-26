<template>
    <div class="panel pie">
        <h2>四川各城市确诊占比</h2>
        <div class="chart"></div>
        <div class="panel-footer"></div>
    </div>
</template>

<script>
    import axios from 'axios'

    export default {
        name: "PanelPie",
        data(){
            return {
                sichuanCityName:'',
                sichuanCityData:''
            }
        },
        methods: {
            myChartPie(sichuanCityData,sichuanCityName) {
                const myChart = this.$echart.init(document.querySelector(".pie .chart"))

                let option = {
                    tooltip: {
                        trigger: "item",
                        formatter: "{a} <br/>{b}: {c} ({d}%)",
                        position: function (p) {
                            //其中p为当前鼠标的位置
                            return [p[0] + 10, p[1] - 10];
                        }
                    },
                    legend: {
                        top: "90%",
                        itemWidth: 10,
                        itemHeight: 10,
                        data: sichuanCityName,
                        textStyle: {
                            color: "rgba(255,255,255,.5)",
                            fontSize: "12"
                        }
                    },
                    series: [
                        {
                            name: "确诊人数",
                            type: "pie",
                            center: ["50%", "42%"],
                            radius: ["40%", "60%"],
                            // color: [
                            //     "#8c3949",
                            //     "#1ad5a5",
                            //     "#0682ab",
                            //     "#0696ab",
                            //     "#06a0ab",
                            //     "#06b4ab",
                            //     "#06c8ab",
                            //     "#06dcab",
                            //     "#06f0ab"
                            // ],
                            label: {show: false},
                            labelLine: {show: false},
                            data: sichuanCityData
                        }
                    ]
                }

                // 使用刚指定的配置项和数据显示图表。
                myChart.setOption(option)
                window.addEventListener("resize", function () {
                    myChart.resize()
                })
            }
        },
        mounted() {
            axios
                .get('/api/right/pie/')
                .then(response => {
                    this.sichuanCityData = response.data.sichuanCityData
                    this.sichuanCityName = response.data.sichuanCityName
                    this.myChartPie(this.sichuanCityData,this.sichuanCityName)
                })

        }
    }
</script>

<style scoped>

</style>