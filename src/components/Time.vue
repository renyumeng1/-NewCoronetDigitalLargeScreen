<template>
    <div class="showTime">
        当前时间：{{time}}
    </div>
</template>

<script>
    import dayjs from 'dayjs'
    export default {
        name: "Time",
        data(){
            return {
                time:''
            }
        },
        methods:{
            getTime(){
                let timeStamp = Date.parse(new Date())
                this.time = dayjs(timeStamp).format('YYYY年MM月DD日 hh:mm:ss')
            }
        },
        mounted() {
            let that = this
            that.timer = setInterval(this.getTime); //开始运行
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
    .showTime {
        position: absolute;
        top: 0;
        right: 0.375rem;
        line-height: 0.9375rem;
        font-size: 0.25rem;
        color: rgba(255, 255, 255, 0.7);
    }
</style>