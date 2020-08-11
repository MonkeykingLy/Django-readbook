import Vue from 'vue'
import App from './App'
import ElementUI from 'element-ui' //Elements-all components of the UI
import 'element-ui/lib/theme-chalk/index.css'//element-ui-css
import router from './router'
import {Message} from 'element-ui'
import axios from 'axios' ;
import Vuex from 'vuex' //Introduce state management
Vue.prototype.$axios= axios ;
Vue.use(Vuex) ;
Vue.prototype.$message = Message
Vue.use(ElementUI) //Using elementUI
Vue.config.productionTip = false

axios.defaults.baseURL = 'http://127.0.0.1:8000/'
//Request interceptor
axios.interceptors.request.use(config => {
  // What do you do before sending a request
  // console.log(config)
  if (window.localStorage.getItem('token')) {
    config.headers.Authorization = window.localStorage.getItem('token')
  }
  return config
},
error => {
  return Promise.reject(error);
});

// Response interceptor
axios.interceptors.response.use(res => {
  // Data processing after a successful request
  return res
}, err=>{
  // Logical processing in response to an error
  return Promise.reject(err.response)
})

new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>',
  render: h => h(App),
}).$mount('#app')
