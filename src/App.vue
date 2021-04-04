<template>
  <div id="nav">
    <router-link :to="{name:'Notas'}">Notas</router-link>
    |
    <router-link :to="{name:'NotaForm'}">Crear nota</router-link>
    |
    <router-link :to="{name:'Todos'}">Todos (API)</router-link>
    |
    <router-link :to="{name:'TodosWS'}">Todos (WS)</router-link>
    |
    <router-link :to="{name:'Rooms'}">Chats</router-link>
    |
    <span v-if="isAuth">
      Hola {{user.username}}
      |
      <a href="#" @click="logout">Logout</a>
    </span>
    <span v-else>
      <router-link :to="{name:'Login'}">Login</router-link> 
      |
      <router-link :to="{name:'Register'}">Registrarse</router-link> 
    </span>


  </div>
  <div v-if="messages.length > 0" class="list-group">
    <div v-for="(message, index) in messages" :key="index" class="alert alert-info" role="alert">
      {{message}}
      <button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
      </button>
    </div>
  </div>
  <div v-if="status == 'success' | status == 'not log'">
    <router-view/>
  </div>
  <div v-else-if="status == 'loading'">
    Cargando
  </div>
  <div v-else-if="status == 'error'">
    Error
  </div>
</template>
<script>
export default {
  name:"App",
  data(){
    return{
    }
  },
  methods:{
    logout(){
      this.$store.commit("logout")
      this.$router.push({name:"Notas"});
    },
    getToken(){
      if(this.token != null){
        this.axios.post("/get-token/", {
          method:"POST",
          token:this.$store.state.token,
        }, {
          headers:{"Authorization":"Token " + this.$store.state.token}})
          .then(response=>{
            console.log("getToken", response);
            this.$store.commit("login", response.data)
          })
      }
    }
  },
  computed:{
    status() {
      return this.$store.state.status
    },
    isAuth(){
      return this.$store.state.token != null && this.$store.state.user != null
    },
    user(){
      return this.$store.state.user
    },
    token(){
      return this.$store.state.token
    },
    messages(){
      return this.$store.state.messages
    }
  },
  created(){
  },
  beforeCreate(){
    this.$store.dispatch("getToken", this.axios)
  },
  mounted(){
    // this.$store.dispatch("setWs")
  }
}
</script>
<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
