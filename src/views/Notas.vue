<template>
  <div v-if="nota != null">
    <Nota :nota="nota"></Nota>
    <floating-button @click.prevent="back"></floating-button>
  </div>
  <div v-else class="notas container">
    <div class="row">
        <div :key="nota.id" v-for="nota in notas" class="col">
            <div class="card">
                <div class="card-header">
                    Notas
                    {{nota.titulo}}
                </div>
                <div class="card-body">
                    <p class="card-text" v-html="cuerpoSinImg(nota.cuerpo)"></p>
                    <button @click="select(nota)" class="btn btn-sm btn-success">Abrir</button>
                </div>
            </div>
        </div>
    </div>
  </div>
</template>

<script>
import Nota from "../components/Nota.vue";
import FloatingButton from "../components/FloatingButton.vue";


export default {
  name: 'Notas',
  components:{
    "Nota":Nota,
    FloatingButton,
  },
  data(){
    return {
      notas:null,
      nota:null,
    }
  },
  computed:{
  },
  methods:{
    back(){
      this.nota=null;
      this.getNotas();
    },
    cuerpoSinImg(cuerpo){
      return cuerpo.replace(/<img[^>]*>/g, "")
    },
    select(nota){
      this.nota = nota;
    },
    getNotas(){
      this.axios.get("/nota/").then(data=>{this.notas=data.data;console.log(data.data)})
      }
  },
  created(){
    this.getNotas();
  },
}
</script>
