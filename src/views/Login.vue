<template>
  <div class="login container">
      <h1>Login</h1>
      <form method="post" @submit.prevent="login">
        <div class="form-group">
          <label for="id_username">Usuario</label>
          <input type="text" v-model="username" name="username" id="id_username" autocomplete="current-username" class="form-control">
        </div>
        <div class="form-group">
          <label for="id_password">Contraseña</label>
          <input type="password" name="password" v-model="password" id="id_password" autocomplete="current-password" class="form-control">
        </div>
        <input type="submit" value="Login" class="btn btn-lg btn-success">
      </form>
  </div>
</template>
  
<script>
export default {
  name: 'Login',
  data(){
    return{
      username:"",
      password:"",
    }
  },
  computed:{
    
  },
  methods:{
    login(){
      console.log("Login");
      this.axios.post("/auth/", {
        username:this.username,
        password:this.password,
      }, {headers:{""}}).then(response=>{
        console.log(response);
        localStorage.setItem('token', response.data.token);
        this.$store.commit("login", response.data)
        this.$store.dispatch("setWs")
        this.$router.push({name:"Notas"});
      })
    }
  },
}
</script>
