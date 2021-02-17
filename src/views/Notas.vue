<template>
  <div v-if="nota != null">
    <button @click="this.nota=null;getNotas();">Back</button>
    <Nota :nota="nota"></Nota>
  </div>
  <div v-else class="notas">
    <div :key="nota.id" v-for="nota in notas">
          Notas
          {{nota.titulo}}
          <button @click="select(nota)">Select</button>
    </div>
    {{test}}
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
      test:this.$store.state.name,
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
