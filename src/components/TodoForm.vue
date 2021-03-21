<template>
    <form @submit.prevent="submitForm">
        <div class="form-group row">

        <label for="titulo" class="col-1 col-form-label">
            ToDo: 
        </label>
        <div class="col">
            <input type="text" v-model="titulo" id="titulo" class="form-control" placeholder="tarea pendiente">
        </div>
        <div class="col-1">
            <input type="submit" value="Crear" class="btn btn-success">
        </div>
        </div>
    </form>
</template>

<script>
export default {
    name: "TodoForm",
    emits:["todoCreated"],
    data(){
        return{
            titulo:"",
        }
    },
    methods:{
        submitForm(){
            this.axios.post("/todos/", {
                user: this.user.id,
                title: this.titulo,
            }, {headers:{
                Authorization: "Token " + this.token,
            }})
            .then(response => {
                console.log(response)
                this.$emit("todoCreated", response.data)
                this.titulo = ""
            })
            .catch(error => console.log(error))
        }
    },
    
  computed: {
    token() {
      return this.$store.state.token;
    },
    user() {
      return this.$store.state.user;
    },
  },
}
</script>