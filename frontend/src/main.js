import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import App from './App'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import router from './router'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faUpload, faPlay, faCheck, faSave, faTrash} from '@fortawesome/free-solid-svg-icons'
import bFormSlider from 'vue-bootstrap-slider'

library.add(faUpload, faPlay, faCheck, faSave, faTrash)

Vue.component('font-awesome-icon', FontAwesomeIcon)

Vue.use(bFormSlider)

Vue.use(BootstrapVue)

Vue.config.productionTip = false

export const EventBus = new Vue()

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  render: h => h(App)
})
