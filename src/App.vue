<template>
  <div id="nav">
    <router-link :to="{name:'Notas'}">Notas</router-link>
    |
    <router-link :to="{name:'Rooms'}">Rooms</router-link>
    |
    <router-link :to="{name:'NotaForm'}">Crear nota</router-link>
    |
    <span v-if="isAuth">
      <a href="#" @click="logout">Logout</a>
    </span>
    <span v-else>
      <router-link :to="{name:'Login'}">Login</router-link> 
    </span>

  </div>
  <router-view/>
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
      if(this.$store.state.token != null){
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
    isAuth(){
      return this.$store.state.token != null 
    },
    user(){
      return this.$store.state.user
    },
    token(){
      return this.$store.state.token
    },
  },
  mounted(){
    this.getToken();
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
