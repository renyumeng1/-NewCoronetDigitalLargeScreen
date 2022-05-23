<template>
    <div class="panel bar1" style="height: 7.75rem">
        <h2>{{ provinceName }}省各市确诊排行（累计）</h2>
        <dv-scroll-ranking-board :config="config" style="width:500px;height:350px"/>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: "PanelBar",
    data() {
        return {
            provinceName: '四川',
            config: {
                data: [
                    {
                        value: 55,
                        name: '周口'

                    },
                    {
                        name: '南阳',
                        value: 120
                    },
                    {
                        name: '西峡',
                        value: 78
                    },
                    {
                        name: '驻马店',
                        value: 66
                    },
                    {
                        name: '新乡',
                        value: 80
                    },
                    {
                        name: '信阳',
                        value: 45
                    },
                    {
                        name: '漯河',
                        value: 29
                    }
                ]
            }
        }
    },
    methods: {
        getProvinceName(provinceName) {
            this.provinceName = provinceName
        },
        getSichuanData() {
            axios
                .get('/api/right/top/')
                .then(response => {
                    this.config = {
                        data: response.data['sichuanCityData']
                    }
                })
        },
        postSichuanData(provinceName) {
            axios
                .post('/api/right/top/change/', JSON.stringify({
                    provinceName: provinceName
                }))
                .then(response => {
                    this.config = {
                        data: response.data['newProvinceData'],
                        sort: false
                    }
                })
        }

    },
    mounted() {
        this.getSichuanData()
        this.$bus.$on('sendProvinceName', this.getProvinceName)
    },
    watch: {
        provinceName(newProvinceName) {
            this.postSichuanData(newProvinceName)
        }
    }

}
</script>

<style scoped>

</style>