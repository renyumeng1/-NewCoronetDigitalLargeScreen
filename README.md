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

Time组件为Header组件的<font color='red'>子组件</font>，我们要**做到时间实时刷新，并且要与现在的时间同步**，那么可以使用`Date.parse(new Date())`获取当前时间戳，并且通过dayjs这个第三方库将时间转换成`YYYY年MM月DD日 hh:mm:ss`，然后在`mounted`这个生命周期钩子里面开启定时器，并在`beforeDestroy`这个生命周期钩子里面摧毁定时器，此时Time的结构为（<font color='red'>css部分忽略</font>）：

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

1. 可视化部分：用到了echarts，但要在Vue中全局使用echarts需要在`main.js`文件中引用echarts并且在Vue的`protptype`属性中挂载一个全局变量`$echart`为echarts即`Vue.prototype.$echart = echarts`，这样所有组件都能使用`this.$echart`访问到echarts
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

###### 5.2.2.1 `PannelBar.vue`

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

接下来都是繁琐的数据处理过程，详见代码（PannelBar部分后端代码）:

```python
# left_pie_panel
topData = data_xinlang["jwsrTop"]  # top10数据
topCityName = []  # top10城市名字
topCityData = []  # top10城市数据
for i in range(len(topData)):
    topCityName.append(topData[i]['name'])
    topCityData.append(int(topData[i]['jwsrNum']))
```

然后将处理好的数据封装到data_total这个字典里，配置后端的路由为`'/api/total/'`，再返回JSON给前端。

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

在PanelBar组件中，通过**mounted这个生命周期钩子**，使用axios向后端发送一个get请求，就可以请求回后端封装的api，我们要做到响应式，就必须得在这个组件监测到数据变化的时候重新渲染页面，而Vue这个框架恰好就能实现这个过程，所以我们现在要做的就是这两步：让Vue监测到数据改变-->重新渲染页面，那么Vue是怎么实现这个过程的呢？Vue是**一个半编译半运行的框架**，在一个xxx.vue文件中，Vue首先通过编译器编译`<template></template>`标签下的内容，编译成Vue的渲染器能识别的虚拟DOM（**用javascript描述的DOM节点**）然后通过Vue的渲染器，让他**递归的**生成真实DOM，这里就只简单说一下Vue的响应式系统。当你在data这个配置项中配置好了数据之后，Vue就会为他代理一个全新的数据，为了方便描述，使用**objectData**来描述这个被代理的对象。（ps：在Vue2中采用了`Object.defineProperty`（对象属性拦截），在Vue3中采用了`Proxy`（对象整体拦截））然后我们把渲染页面这一系列操作统称为：**副作用函数**(副作用函数指的就是，当这个函数被调用之后会对**整个页面产生影响的函数**，例如：修改了文本内容，样式，页面上的某一个元素....) 当我访问`objectData`中的某个字段时，Vue就会通过`Proxy`的`get`拦截我这个访问，然后将**副作用函数**放在一个bucket（可以简单的抽象成一个桶）里，然后当用户修改`objectData`的某个字段时，Vue也会通过`Proxy`的`set`拦截这个访问，最后在**用户修改之后重新调用副作用函数。**接下来是**响应式系统的简单实现**：

```javascript
//副作用函数
function effect() {
        document.body.innerText = obj.text
    }

    const bucket = new Set()
    const data = {
        text: 'hello world'
    }
    
    //数据代理
    const obj = new Proxy(data, {
        get(target, key) {
            bucket.add(effect)
            return target[key]
        },

        set(target, key, newValue) {
            target[key] = newValue
            bucket.forEach(fn => fn())
        }
    })

    effect()
//m
    setTimeout(() => {
        obj.text = 'hello vue'
    }, 1000)
```

当我们请求回后端的数据之后，就可以将请求回的数据挂载到data中配置好的数据项上（Vue会事先将在data这个配置项中的配置的引用，进行<font color='red'>数据代理</font>了之后，再**挂载到VueComponent**上，所以我们就可以使用`this.dataName`访问到这些引用），此后，调用在methods里配置好的`myChartBar`函数（methods里配置好的函数同样会被挂载到`VueComponent`上），并且将这些数据作为参数传进这个函数，此时，Vue就会为我们重新渲染一次页面，并且把这个柱状图渲染到容器里。`PannelBar`的完整代码如下（<font color='red'>css部分忽视</font>）：

```vue
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
```

这个组件还有个部分，在打开这个可视化大屏时，如果数据还没有请求回来，页面就会显示Loading。我在`watch`里配置了一个`tempBar`（boolean），监测数据的请求情况，如果请求回了数据，`tempBar`就会被修改为`false`，当`tempBar`的值改变了之后，就会触发`watch`里的`tempBar`函数，那么就会延时2秒向`App.Vue`传递`tempBar`，此时Vue的一个指令,`v-if`就派上用场了，他可以显示（隐藏）一个DOM节点，`app.vue`组件代码如下：

```vue
<template>
    <div>
        <dv-full-screen-container>
            <dv-loading v-if="showLoading">Loading...</dv-loading>
            <Header/>
            <AllCharts/>
        </dv-full-screen-container>

    </div>

</template>

<script>

import Header from "@/components/Header";
import AllCharts from "@/components/AllCharts";

export default {
    name: 'App',
    components: {
        AllCharts,
        Header,
    },
    data() {
        return {
            showLoading: true,
        }
    },
    methods:{
        getBarTemp(BarTemp){
            this.showLoading = BarTemp
        }
    },
    mounted() {
        this.$bus.$on('getBarTemp',this.getBarTemp)
    }
}
</script>
```

###### 5.2.2.2 `PannelLine.vue`

`PannelLine`的前端部分的设计思路和`PannelBar`差不多，不同就是封装的数据类型不一样，`PannelLine`需要的是如下数据：

```javascript
data() {
        return {
            confirms: '',
            dates: '',
            deads: '',
            heals: '',
            storeConfirms: '',
        }
    }
```

分别是无症状人数，治愈人数，日期，死亡人数和确诊人数。通过`axios`异步往后端的`'/api/left/line/'`请求回需要的设计，这部分组件就完成了。

###### 5.2.2.3 `Shuffling.vue`

这个组件展示的是全国各省各市疫情的情况，但默认他是展示一个省的所有市的，所以，他和中间疫情分布图部分做了交互，即，点击了地图上某一个省，就展示某个省所有市的情况。

在这个组件中，用到了`dataV`的`dv-scroll-board`组件，这个组件为我们封装好展示轮播表的所有代码，我们只用使用`Vue`的`prop`属性往组件里传参就行了。代码如下

```vue
<div>
        <div class="panel">
            <h2>{{ provinceName }}省各市疫情累计情况</h2>
            <dv-scroll-board
                :config="config"
                style="height: 100%;width: 100%"
            />
        </div>
```

`config`是传入的配置对象，包含展示的数据和对轮播表的调整，具体参数可以去官方文档查阅。与`Map`组件的交互部分的设计思路如下：

当`Map`组件监测到用户点击了地图上的某一个省份时，`Map`组件就会把点击的省份的`provinceName`传递给`Shuffling`组件，同样`Shuffling`也监测着`provinceName`的变化，当接收到`Map`组件的数据时，意味着`Shuffling`组件的`provinceName`发生了变化，这个时候，再把这个`provinceName`发送给后端，而后端接收到请求之后，检索这个`provinceName`然后再将包含这个`provinceName`的所有字段的数据封装成`JSON`再传回给前端。

前端部分代码如下：

```javascript
	methods: {
        getAlldata() {
            axios
                .get('/api/right/shuffling/')
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
```

后端部分代码如下：

```python
@app.route('/api/left/shuffling/change/', methods=['POST'])
def change_right_shuffling():
    provinceName = request.get_data()
    provinceName = json.loads(provinceName)
    provinceName = provinceName['provinceName']
    city_data = filter_data(provinceName)
    city_value = get_shuffling_data(city_data)
    data_total = {
        "provinceName": provinceName,
        "newData": city_value
    }
    return jsonify(data_total)
```

##### 5.2.3 `Middle.vue`组件

这个组件包含两个子组件：

1. `Map.vue`组件
2. `Total.vue`组件

###### 5.2.3.1 `Map.vue`

这个组件是在地图上展示中国疫情的分布图，同时也和轮播表，饼状图做了交互，部分代码如下：

```vue
<template>
    <div class="map">
        <div class="chart"></div>
        <div class="map1"></div>
        <div class="map2"></div>
        <div class="map3"></div>
    </div>
</template>

<script>
import '../../assets/js/china'
import axios from 'axios'

export default {
    name: "Map",
    data(){
        return {
            mapData:'',
            provinceName:''
        }
    },
    methods: {
        myChartMap(mapData) {
            // 1. 实例化对象
            const myChart = this.$echart.init(document.querySelector(".map .chart"));
            let option = {
                title: {
                    text: "中国疫情分布图（累计）",
                    left: 250, //设置标题的距离盒子左边的距离
                    top: 100, //设置标题距离盒子顶部的距离
                    color:'#a61919'
                },

                series: [
                    {
                        name: "确诊人数", //控制鼠标hover上去显示的固定文本
                        type: "map", //告诉echarts需要渲染一个地图
                        mapType: "china", //告诉echarts要渲染注册的china地图
                        label: {
                            show: true, //控制是否显示省份的名称
                            color: "white" // 设置显示每个省份的字体颜色
                        },
                        itemStyle: {
                            borderColor: "green" //每个省份的边界的颜色
                        },
                        emphasis: { //控制鼠标移入的版块的颜色
                            color: "#fff", //移入该模块的字体颜色
                            itemStyle: {
                                areaColor: "#83b5e7", //鼠标hover到模块上的背景色
                            }
                        },
                        zoom: 1.2, //控制整个地图的缩放倍数
                        data: mapData //TODO 每个板块的数据TODO
                    }

                ],
                visualMap: [{
                    type: "piecewise", //左下角的分段显示
                    show: true,
                    splitNumber: 4, //显示几个分段
                    pieces: [ //左下角的自定义分段显示
                        {min: 15000},
                        {min: 900, max: 15000},
                        {min: 310, max: 900},
                        {min: 200, max: 310},
                        {min: 0, max: 200}],

                    align: "right",
                    left: 0,
                    top: 550,
                    inRange: {
                        symbol: "circle",
                        color: ["#ffc0b1", "#9c0505"]
                    }
                }],
                tooltip: {
                    trigger: "item",
                    formatter: function (params) {
                        return params.name + "<br/>" + params.seriesName + "：" + params.value
                    }
                },
            }
            myChart.setOption(option)
            myChart.on('click',params =>{
                this.provinceName = params.data.name
                this.$bus.$emit('sendProvinceName',this.provinceName)
            })
            window.addEventListener("resize", function () {
                myChart.resize();
            });
        }
    },
    mounted() {
        axios
            .get('/api/right/map/')
            .then(response => {
                this.mapData = response.data.mapData
                this.myChartMap(this.mapData)
            })
    }
}
</script>
```

###### 5.2.3.2 `Total.vue`

这个组件是为了展示中国现有疫情情况，部分代码如下：

```vue
<template>
    <div class="no">
        <div class="no-hd">
            <ul>
                <li>{{ gnTotal }}</li>
                <li style="color: red">{{ deathTotal }}</li>
            </ul>
        </div>
        <div class="no-bd">
            <ul>
                <li>国内现有确诊</li>
                <li>国内累计死亡</li>
            </ul>
        </div>
        <div class="no-hd">
            <ul>
                <li>{{ addConNew }}</li>
                <li style="color: red">{{ addDeathNew }}</li>
            </ul>
        </div>
        <div class="no-bd">
            <ul>
                <li>至今累计新增确诊</li>
                <li>至今累计新增死亡</li>
            </ul>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    // eslint-disable-next-line vue/multi-word-component-names
    name: "Total",
    data() {
        return {
            gnTotal: '',
            deathTotal: '',
            theTime: '',
            addConNew: '',
            addDeathNew: '',
        }
    },
    methods: {
        getTotalData() {
            axios
                .get("/api/total/")
                .then(response => {
                    this.gnTotal = response.data.gnTotal
                    this.deathTotal = response.data.deathTotal
                    this.addConNew = response.data.addConNew
                    this.addDeathNew = response.data.addDeathNew
                    let getTime = response.data.times
                    this.theTime = getTime
                    this.$bus.$emit("getTime", getTime)
                })
                .catch(error => console.log(error.message))
        },
        getTime() {
            axios
                .get("/api/total/")
                .then(response => {
                    this.theTime = response.data.times
                })
        }
    },
    watch: {
        // 监测time的变化，变化了延时1分钟请求其他数据
        theTime() {
            clearTimeout(this.timer)
            this.timer = setTimeout(() => {
                this.getTotalData()
            }, 60)
        }
    },
    mounted() {
        this.getTotalData()
        //定时器1小时请求一次time
        this.timerGetTime = setInterval(this.getTime, 3600000)
    },
    beforeDestroy() {
        clearInterval(this.timerGetTime)
    }

}
</script>
```

