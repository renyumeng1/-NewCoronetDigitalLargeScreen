import Vue from 'vue'
import App from './App.vue'
import 'lib-flexible/flexible'
import eCharts from 'echarts'

Vue.config.productionTip = false
Vue.prototype.$echart = eCharts


new Vue({
  render: h => h(App),
  beforeCreate() {
    Vue.prototype.$bus = this
  }
}).$mount('#app')
