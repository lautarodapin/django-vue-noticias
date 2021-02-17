<template>
  <div class="nota">
    <h1>
      {{nota.titulo}}
    </h1>
    <h4>{{nota.subtitulo}}</h4>
    <h5>{{nota.created_at}}</h5>
    <h6>
      {{nota.slug}}
    </h6>
    <p>{{nota.cuerpo}}</p>
    <Comentario v-for="(comentario, index) in nota.comentarios" :comentario="comentario" :key="index"></Comentario>
    <form v-if="isAuth" @submit.prevent="postComentario" method="post">
      <textarea v-model="comentario"  rows="3"></textarea>
      <input type="submit" value="Comentar">
    </form>
  </div>
</template>

<script>
import Comentario from './Comentario.vue';

export default {
  name: 'Nota',
  components:{Comentario:Comentario},
  props:{
    nota:Object,
  },
  data(){
    return {
      comentario:"",
    }
  },
  computed:{
    isAuth(){
      return this.$store.state.token != null 
    }
  },
  methods:{
    postComentario(){
      this.axios.post('http://127.0.0.1:8000/api/comentario/', {
        cuerpo:this.comentario,
        nota:this.$props.nota.slug,
      }, {headers:{"Authorization":`Token ${localStorage.getItem('token')}`}})
      .then(response=>{
        console.log(response);
        this.$props.nota.comentarios = [...this.$props.nota.comentarios, response.data];
        this.comentario = "";
      })
    },
    getNota(){
      this.axios.get(`http://127.0.0.1:8000/api/nota/${this.$props.nota.slug}/`).then(response=>{this.$props.nota = response.data; console.log(response)});
    }
  },
  created(){
    this.getNota();
  },
}
</script>
