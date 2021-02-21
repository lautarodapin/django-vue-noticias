<template>
  <div class="nota">
    <div class="jumbotron jumbotron-fluid">
      <div class="container">
        <h1 class="display-4">
            {{nota.titulo}}
          
        </h1>
        <h1 class="display-6 text-muted">
            {{nota.subtitulo}}
        </h1>
        <h5>{{nota.created_at}}</h5>
      </div>
    </div>
    <p class="lead">
        {{nota.cuerpo}}

    </p>
    <hr>
    <h6 class="lead">Comentarios</h6>
    <div class="row">
        <div class="col-12" v-for="(comentario, index) in nota.comentarios" :key="index">
            <Comentario  :comentario="comentario" ></Comentario>
        </div>
        <div class="col-12">
            <form v-if="isAuth" @submit.prevent="postComentario" method="post">
                <div class="form-group">
                    <textarea v-model="comentario"  rows="3" class="form-control" placeholder="Comentario..."></textarea>
                </div>
                <input type="submit" class="btn btn-sm btn-success" value="Comentar">
            </form>
        </div>
    </div>
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
