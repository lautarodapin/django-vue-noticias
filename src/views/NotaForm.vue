<template>
  <div>
    <h4>Nota form</h4>
    <form @submit.prevent="crearNota" method="post">
      <label for="id_titulo">Titulo</label>
      <input type="text" v-model="titulo" id="id_titulo">
      <label for="id_subtitulo">Subtitulo</label>
      <input type="text" v-model="subtitulo" id="id_subtitulo">
      <label for="id_cuerpo">Cuerpo</label>
      <textarea v-model="cuerpo" id="id_cuerpo" rows="10"></textarea>
      <!-- <quill-editor
        :content="content"
        :options="editorOption"
        @change="onEditorChange($event)"
      ></quill-editor> -->
      <input type="submit" value="Crear">
    </form>
  </div>
</template>

<script>
import 'quill/dist/quill.core.css'
import 'quill/dist/quill.snow.css'
import 'quill/dist/quill.bubble.css'
// import { quillEditor } from 'vue-quill-editor'

export default {
  name: 'NotaForm',
  components:{
    // quillEditor
  },
  data(){
    return {
      content:"",
      editorOption: {},
      titulo:"",
      subtitulo:"",
      cuerpo:"",
    }
  },
  methods:{
    onEditorChange({ quill, html, text }){
        console.log('editor change!', quill, html, text)
        this.content = html
    },
    crearNota(){
      console.log("Crear nota");
      const data = {
        titulo:this.titulo,
        subtitulo:this.subtitulo,
        cuerpo:this.cuerpo,
        autor:this.$store.state.user.id,
      }
      console.log(data);
      this.axios.post('/nota/', data, {
        headers:{
          "Authorization":"Token " + this.$store.state.token,
        }
      }).then(response=>{
        console.log(response)
      })
    },
  },
  created(){
  },
}
</script>
