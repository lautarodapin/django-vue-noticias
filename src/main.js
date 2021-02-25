import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'
import VueAxios from 'vue-axios'
import store from './store.js';
import 'bootstrap';


console.log(process.env)

const API_URL = process.env.VUE_APP_API_URL
// import VueQuillEditor from 'vue-quill-editor'
// import 'quill/dist/quill.core.css' // import styles
// import 'quill/dist/quill.snow.css' // for snow theme
// import 'quill/dist/quill.bubble.css' // for bubble theme


const app = createApp(App).use(store)
    .use(router)
    .use(VueAxios, axios)
    .use(store)
// .use(VueQuillEditor, /* { default global options } */)
// app.axios.defaults.baseURL = "/api/"
app.axios.defaults.baseURL = API_URL

// QUILL

import { quillEditor } from 'vue3-quill'
app.use(quillEditor)

app.mount('#app')
