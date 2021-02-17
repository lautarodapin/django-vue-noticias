<template>
  <div class="login">
    <h1>Login</h1>
    <form method="post" @submit.prevent="login">
      <label for="id_username">Username</label>
      <input type="text" v-model="username" name="username" id="id_username" autocomplete="username">
      <label for="id_password">Password</label>
      <input type="password" name="password" v-model="password" id="id_password" autocomplete="current-password">
      <input type="submit" value="Login">
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
  methods:{
    login(){
      console.log("Login");
      this.axios.post("/auth/", {
        username:this.username,
        password:this.password,
      }).then(response=>{
        console.log(response);
        localStorage.setItem('token', response.data.token);
        this.$store.commit("login", response.data)
        this.$router.push({name:"Notas"});
      })
    }
  },
}
</script>
