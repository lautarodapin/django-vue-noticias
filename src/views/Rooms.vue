<template>
  <div>
    <div v-for="(room, index) in rooms" :key="index">
      {{room.nombre}} | 
      {{room.host.username}} | 
      <button @click="this.selected=true;this.room=room;this.getRoom();">Entrar</button>
      <!-- TODO no funciona el router link -->
      <!-- <router-link :to="{name:'Room', params:{room:room.pk}}">Rooms</router-link> -->
    </div>
    <hr>
    <form v-if="selected == false" @submit.prevent="createRoom" method="post">
      <h4>Crear nuevo room</h4>
      <label for="id_nombre">Nombre</label>
      <input type="text" name="Nombre" v-model="nombre" id="id_nombre">
      <input type="submit" value="Crear">
    </form>
    <div v-else>
      <button @click="this.selected=false;">Volver</button>
      <h3>{{room.nombre}} | {{room.host.username}}</h3>
      <div class="chat">
        <p v-for="(message, index) in messages" :key="index">
          {{message.created_at_formatted}} | {{message.user_extra.username}}: {{message.text}}
        </p>
        <hr>
        <form @submit.prevent="submitComentario" method="post">
          <textarea name="comentario" id="id_comentario" v-model="comentario"></textarea>
          <input type="submit" value="Comentar">
        </form>
      </div>
    </div>
    <!-- <router-view></router-view> -->
  </div>
</template>

<script>

export default {
  name: 'Rooms',
  components:{
  },
  data(){
    return {
      nombre:"",
      rooms:[],
      selected:false,
      room:null,
      comentario:"",
      messages:[],
    }
  },
  methods:{
    submitComentario(){
      const data = {
        text:this.comentario,
        user:this.user.id,
        room:this.room.pk,
      }
      console.log("Submit comentario", data);
      
      this.axios.post('/messages/', data, {
        headers:{"Authorization": "Token "+this.token}
      }).then(response=>{
        console.log(response);
        this.messages = [...this.messages, response.data]
      });
    },
    getRoom() {
      this.axios
        .get(`/rooms/${this.room.pk}/`)
        .then((response) => {
          console.log(response);
          this.room = response.data;
          this.messages = response.data.messages;
        });
    },
    getRooms(){
      this.axios.get("/rooms/")
      .then(response=>{
        console.log(response);
        this.rooms = response.data;
      });
    },
    createRoom(){
      const data = {
        nombre:this.nombre,
        host:this.user.id,
      }
      this.axios.post("/rooms/", data, {headers:{
        "Authorization": "Token " + this.token,
      }}).then(response=>{
        console.log(response);
        this.rooms.push(response.data)
      })
    }
  },
  computed:{
    token(){
      return this.$store.state.token
    },
    user(){
      return this.$store.state.user
    },
  },
  created(){
    this.getRooms()
  },
}
</script>
