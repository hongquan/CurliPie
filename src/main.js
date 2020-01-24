import Vue from 'vue'
import App from './App.vue'
import router from './router'
import { VueGrid } from '@liqueflies/vue-grid'
import VFC from 'vfc'
import VueLodash from 'vue-lodash'
import VueHighlightJS from 'vue-highlightjs'
import 'vfc/dist/vfc.css'

Vue.use(VFC)
Vue.use(VueGrid)
Vue.use(VueLodash)
Vue.use(VueHighlightJS)
Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
