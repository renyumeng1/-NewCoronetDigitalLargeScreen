<template>
    <div>
        <div class="panel">
            <h2>{{ provinceName }}省各市疫情累计情况</h2>
            <dv-scroll-board
                :config="config"
                style="height: 100%;width: 100%"

            />
        </div>
        <div class="panel-footer"></div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: "Shuffling",
    data() {
        return {
            config: '',
            provinceName: '四川'
        }
    },
    methods: {
        getAlldata() {
            axios
                .get('/api/left/shuffling/')
                .then(response => {
                    this.config = {
                        data: response.data.PanelShufflingData,
                        waitTime: 1500,
                        header: ['城市名', '确诊', '治愈', '死亡'],
                        //headerBGC: "FFFFFF0A",
                        oddRowBGC: "FFFFFF0A",
                    }
                })
        },
        getProvince(provinceName) {
            this.provinceName = provinceName
        }
    },
    mounted() {
        this.getAlldata()
        this.$bus.$on('sendProvinceName', this.getProvince)
    },
    watch: {
        provinceName(data) {
            axios
                .post('/api/left/shuffling/change/', JSON.stringify({
                    provinceName: data
                }))
                .then(response => {
                    this.config = {
                        data: response.data.newData,
                        waitTime: 1500,
                        header: ['城市名', '确诊', '治愈', '死亡'],
                        oddRowBGC: "FFFFFF0A",
                    }
                })
                .catch(error => {
                    console.log(error.message)
                })
        }
    },
    beforeDestroy() {
        this.$bus.$off('sendProvinceName')
    }
}
</script>

<style scoped>

</style>