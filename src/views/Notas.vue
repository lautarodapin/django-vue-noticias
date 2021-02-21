<template>
  <div v-if="nota != null">
    <button @click="this.nota=null;getNotas();" class="btn btn-sm btn-success">Volver</button>
    <Nota :nota="nota"></Nota>
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
                    <p class="card-tex">
                        {{nota.cuerpo}}
                    </p>
                    <button @click="select(nota)" class="btn btn-sm btn-success">Abrir</button>
                </div>
            </div>
        </div>
    </div>
  </div>
</template>

<script>
import Nota from "../components/Nota.vue";

export default {
  name: 'Notas',
  components:{
    "Nota":Nota,
  },
  data(){
    return {
      notas:null,
      nota:null,
    }
  },
  methods:{
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
