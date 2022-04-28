# frontend

## 1.Project setup
```
npm install
```

### 2.Compiles and hot-reloads for development
```
npm run serve
```

### 3.Compiles and minifies for production
```
npm run build
```

### 4.Technology stack
前端：Vue+data-V+axios+echarts+flexible

脚手架：Vue cli

后端：flask

数据来源：新浪和网易的疫情数据api

### 5.Frontend and backend structure

项目结构（组件部分）：

```
G:.
│   AllCharts.vue
│   Header.vue
│   Left.vue
│   Middle.vue
│   Right.vue
│   Time.vue
│
├───LeftPanel
│       PanelBar.vue
│       PanelLine.vue
│       Shuffling.vue
│
├───MiddlePanel
│       Map.vue
│       Total.vue
│
└───RightPanel
        PanelBar.vue
        PanelLine.vue
        PanelPie.vue
```



设计思路：

用flexible将页面分割成24个部分，然后将整体元素拆分成两个大的组件：

1. Header部分
2. AllCharts部分

### 5.1 Header部分设计思路

为了方便维护代码，将Header的时间显示拆分成Header的一个子组件,所以现在Header的结构为（<font color='red'>css部分忽略</font>）：

```vue
//Header.vue
<template>
    <div>
        <header>
            <h1>中国疫情变化（{{StatisticalTime}}）</h1>
            <Time/>
        </header>
    </div>
</template>

<script>
    import Time from "@/components/Time";
import axios from 'axios'

export default {
    // eslint-disable-next-line vue/multi-word-component-names
    name: "Header",
    components: {
        Time,
    },
    data() {
        return {
            StatisticalTime: ''
        }
    },
    mounted() {
        this.$bus.$on('getTime', time => {
            this.StatisticalTime = time
        })

    },
    beforeDestroy() {
        this.$bus.$off('getTime')
    }

}
</script>
```

所以Time组件为Header组件的<font color='red'>子组件</font>，我们要**做到时间实时刷新，并且要与现在的时间同步**，那么可以使用`Date.parse(new Date())`获取当前时间戳，并且通过dayjs这个第三方库将时间转换成`YYYY年MM月DD日 hh:mm:ss`，然后在`mounted`这个生命周期钩子里面开启定时器，并在`beforeDestroy`这个生命周期钩子里面摧毁定时器，此时Time的结构为（<font color='red'>css部分忽略</font>）：

```vue
//Time.vue
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
```

此时Header部分已经开发完成，但是我们还没有向后端请求数据，也没有开始设计后端数据接口。<font color='red'>（统计截止时间是别的组件（leftPanelPie）传过来的数据）</font>

### 5.2 allCharts部分设计思路



