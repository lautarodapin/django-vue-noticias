<template>
  <div class="login container">
      <h1>Registrar</h1>
      <form method="post" @submit.prevent="register">
        <div class="form-group">
          <label for="id_username">Usuario</label>
          <input type="text" v-model="username" name="username" id="id_username" autocomplete="current-username" class="form-control">
        </div>
        <div class="form-group">
          <label for="id_password">Contraseña</label>
          <input type="password" name="password" v-model="password" id="id_password" autocomplete="current-password" class="form-control">
        </div>
        <input type="submit" value="Registrarse" class="btn btn-lg btn-success">
      </form>
  </div>
</template>
  
<script>
export default {
  name: 'Register',
  data(){
    return{
      username:"",
      password:"",
    }
  },
  computed:{
    
  },
  methods:{
    register(){
      console.log("Register");
      this.axios.post("/users/", {
        username:this.username,
        password:this.password,
      }).then(response=>{
        console.log(response);
        localStorage.setItem('token', response.data.token);
        this.$store.commit("login", {user:response.data, token:response.data.token})
        this.$store.dispatch("setWs")
        this.$router.push({name:"Notas"});
      })
    }
  },
}
</script>
