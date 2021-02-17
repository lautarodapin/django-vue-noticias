import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'
import VueAxios from 'vue-axios'
import store from './store.js';

// import VueQuillEditor from 'vue-quill-editor'
// import 'quill/dist/quill.core.css' // import styles
// import 'quill/dist/quill.snow.css' // for snow theme
// import 'quill/dist/quill.bubble.css' // for bubble theme


const app = createApp(App).use(store)
    .use(router)
    .use(VueAxios, axios)
    .use(store)
// .use(VueQuillEditor, /* { default global options } */)
app.axios.defaults.baseURL = "http://127.0.0.1:8000/api/"

app.mount('#app')
