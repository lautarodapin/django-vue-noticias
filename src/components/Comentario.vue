<template>
  <div class="comentario">
        {{comentario.created_at}} - {{comentario.autor.username}}: {{comentario.cuerpo}}
  </div>
</template>

<script>

export default {
  name: 'Comentario',
  props:{
    comentario:Object,
  },
  data(){
    return {
    }
  },
  methods:{
  },
  created(){
    
  },
}
</script>
