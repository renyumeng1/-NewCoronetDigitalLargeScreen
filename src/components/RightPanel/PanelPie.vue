<template>
    <div class="panel pie">
        <h2>{{ provinceName }}各城市（区）确诊占比</h2>
        <div class="chart"></div>
        <div class="panel-footer"></div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: "PanelPie",
    data() {
        return {
            CityName: '',
            CityData: '',
            provinceName: '四川'
        }
    },
    methods: {
        myChartPie(CityData, CityName) {
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
                    data: CityName,
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
                        label: {show: true},
                        labelLine: {show: true},
                        data: CityData
                    }
                ]
            }

            // 使用刚指定的配置项和数据显示图表。
            myChart.setOption(option)
            window.addEventListener("resize", function () {
                myChart.resize()
            })
        },
        getProvince(provinceName) {
            this.provinceName = provinceName
        }
    },
    mounted() {
        axios
            .get('/api/right/pie/')
            .then(response => {
                this.CityData = response.data.sichuanCityData
                this.CityName = response.data.sichuanCityName
                this.myChartPie(this.CityData, this.CityName)
            })
        this.$bus.$on('sendProvinceName', this.getProvince)

    },
    beforeDestroy() {
    },
    watch: {
        provinceName(data) {
            axios
                .post('/api/right/pie/change/', JSON.stringify({
                    provinceName: data
                }))
                .then(response => {
                        this.CityData = response.data.newData
                        this.CityName = response.data.provinceName
                        this.$echart.init(document.querySelector(".pie .chart")).dispose()
                        this.myChartPie(this.CityData, this.CityName)
                    }
                )
                .catch(error => {
                    console.log(error.message)
                })
        }
    },
}
</script>

<style scoped>

</style>