<template>
  <div class="container">
    <h4>Nota form</h4>
    <form @submit.prevent="crearNota" method="post">
      <div v-if="errors.length > 0" class="list-group">
        <div v-for="(error, index) in errors" :key="index" class="alert alert-warning alert-dismissible fade show" role="alert">
            {{error}}
        </div>
      </div>      
      <div class="form-group">
        <label for="id_titulo">Titulo</label>
        <input type="text" v-model="titulo" id="id_titulo" class="form-control">
      </div>
      <div class="form-group">
        <label for="id_subtitulo">Subtitulo</label>
        <input type="text" v-model="subtitulo" id="id_subtitulo" class="form-control">
      </div>
      <div class="form-group">
        <quill-editor
          v-model="cuerpo"
          :options="editorOption"
          style="height:400px;"
          @change="onEditorChange($event)"
        ></quill-editor>
      </div>
      <input type="submit" value="Crear" class="btn btn-lg btn-success">
    </form>
  </div>
</template>

<script>
import { quillEditor } from 'vue3-quill'


export default {
  name: 'NotaForm',
  components:{
    quillEditor
  },
  data(){
    return {
      cuerpo:"",
      editorOption: {},
      titulo:"",
      subtitulo:"",
      errors: [],
    }
  },
  methods:{
    onEditorChange({ quill, html, text }){
        console.log('editor change!', quill, html, text)
        this.cuerpo = html
    },
    cleanForm(){
      this.cuerpo = "";
      this.titulo = "";
      this.subtitulo = "";
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
          "Authorization":"Token " + this.token,
        }
      }).then(response=>{
        console.log(response)
        this.$store.dispatch("addMessage", `Nota "${this.titulo} creada con exito!"`)
        this.cleanForm();
        this.$router.push({
          name:"Notas"
        })
      })
      .catch(error => {
        console.log(error.response)
        var array = []
        for(var key in error.response.data){
          array.push(`${key.toUpperCase()}: ${error.response.data[key]}`)
        }
        this.errors = array
      })
    },
  },
  computed:{
    token(){
      return this.$store.state.token
    }
  },
  created(){
  },
}
</script>
