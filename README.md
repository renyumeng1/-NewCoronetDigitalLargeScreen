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

#### 5.1 Header部分设计思路

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

#### 5.2 allCharts部分设计思路

`allCharts.vue`抽象出了三个子组件，`Left.vue`,`Middle.vue`,`Right.vue`，这三个部分分别是：页面中最左侧的图表，中间的图表，和右边的图表，此时，`allCharts.vue`的结构为（<font color='red'>css部分忽略</font>）：

```vue
// allCharts.vue
<template>
    <div>
        <section class="mainbox">
            <Left/>
            <Middle/>
            <Right/>
        </section>

    </div>
</template>

<script>
    import Left from "@/components/Left";
    import Middle from "@/components/Middle";
    import Right from "@/components/Right";

    export default {
        name: "Section",
        components: {Right, Middle, Left}
    }
</script>
```

##### 5.2.1 准备工作

1. 可视化部分：用到了echarts，但要在Vue中全局使用echarts需要在`main,js`文件中引用echarts并且在Vue的`protptype`属性中新增`$echart`为echarts即`Vue.prototype.$echart = echarts`
2. 全局事件总线：在Vue中不使用Vuex实现组件间通信是一件很麻烦的事，但是在一个小项目中，又没有必要使用Vuex，所以，我们可以找一个中间量，存储需要传递的数据。在Vue的虚拟dom中，每一个组件都是一个新的VueComponent对象，而每一个VueComponent对象的原型对象的属性，都指向了VueModel原型对象，所以我们可以在Vue的原型对象上绑定一个`$bus`属性指向了Vue本身，那么，这个中间变量就实现了。即在`main.js`中，在Vue的beforeCreate这个生命周期钩子中`Vue.prototype.$bus = this`
```vue
   new Vue({
       render: h => h(App),
       beforeCreate() {
           Vue.prototype.$bus = this
       }
```
3. 引入data-v：

```vue
import dataV from '@jiaminghi/data-view'
Vue.use(dataV)
```

`main.js`完整代码

```javascript
import Vue from 'vue'
import App from './App.vue'
import 'lib-flexible/flexible'
import eCharts from 'echarts'
import dataV from '@jiaminghi/data-view'

Vue.use(dataV)
Vue.config.productionTip = false
Vue.prototype.$echart = eCharts

new Vue({
    render: h => h(App),
    beforeCreate() {
        Vue.prototype.$bus = this
    }
}).$mount('#app')
```





##### 5.2.2 `Left.vue`组件

`Left.vue`包含了三个部分，分别是三个图表：内容为中国新冠Top10的柱状图，内容为中国近一个月新冠（感染人数，治愈人数，死亡人数，无症状感染者人数）的折线图，和一个各个省份中**各个城市**的疫情数据（感染人数，治愈人数，死亡人数，无症状感染者人数）轮播图，所以，Left组件又抽象出了三个子组件

1. PannelBar.vue
2. PanelLine.vue
3. Shuffling.vue

此目录的结构为

```
G:.
├───LeftPanel
│       PanelBar.vue
│       PanelLine.vue
│       Shuffling.vue
```

Left.vue的结构为：

```vue
<template>
    <div class="column">
        <PanelBar/>
        <PanelLine/>
        <Shuffling/>
    </div>
</template>

<script>
import PanelBar from "@/components/LeftPanel/PanelBar";
import PanelLine from "@/components/LeftPanel/PanelLine";
import Shuffling from '@/components/LeftPanel/Shuffling'

export default {
    name: "Left",
    components: {Shuffling, PanelLine, PanelBar},


}
</script>
```

###### 5.2.1.1 `PannelBar.vue`

这个组件展示的是关于中国疫情最多的10个城市，现在，开始设计后端的api。通过翻看echarts的文档，我们可以查到，在echarts中，柱状图的数据，需要传入两个array类型的data，所以在设计后端api时，需要返回的数据为如下格式：

```json
{
    cityName:[array],
    cityData:[array],
}
```

在flask框架中，使用requests这个库，向新浪的api（https://interface.sina.cn/news/wap/fymap2020_data.d.json）发送一个get请求，然后我们就拿回了我们需要的所有数据，然后通过json库将json格式的数据反序列化成python的字典。

```python
url_xinlang = "https://interface.sina.cn/news/wap/fymap2020_data.d.json"
r1 = requests.get(url=url_xinlang)
data_get_xinlang = json.loads(r1.text)
data_xinlang = data_get_xinlang["data"]
```

接下来都是繁琐的数据处理过程，详见代码（PannelBar部分后端代码）

```python
# left_pie_panel
topData = data_xinlang["jwsrTop"]  # top10数据
topCityName = []  # top10城市名字
topCityData = []  # top10城市数据
for i in range(len(topData)):
    topCityName.append(topData[i]['name'])
    topCityData.append(int(topData[i]['jwsrNum']))
```

然后将处理好的数据封装到data_total这个字典里配置后端的路由为`'/api/total/'`，再返回JSON给前端。

```python
@app.route('/api/total/')
def total_number():
    data_total = {
        'gnTotal': gnTotal,
        'deathTotal': deathTotal,
        'times': times,
        'addConNew': addConNew,
        'addDeathNew': addDeathNew
    }
    return jsonify(data_total)
```

在PanelBar组件中，通过mounted这个生命周期钩子，通过axios向后端发送一个get请求，就可以请求回后端封装的api，我们要做到响应式，就必须得在这个组件监测到数据变化的时候重新渲染页面，而Vue在虚拟dom中，只要监测到配置项data中的数据发生了改变，就会执行diff算法，重新渲染页面，所以，我们得配置data然后在数据请求成功时，改变data的值
