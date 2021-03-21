<template>
  <div class="container">
    <h3>ToDos de {{ user.username }}</h3>
    <todo-form @todoCreated="(data) => this.todos.push(data)"/>
    <div v-if="todos.length > 0" class="card">
      <ul class="list-group list-group-flush">
        <li class="list-group-item" v-for="todo in todos" :key="todo.id">
          {{ todo.title }}
          <span>
            <small class="text-muted">
              {{ todo.time_since_created }}
            </small>
          </span>
          <span v-if="todo.is_done == false">
            <Pending/>
            <button @click="markAsDone(todo)" class="btn btn-sm btn-secondary">
              DONE
            </button>
          </span>
        </li>
      </ul>
    </div>
    <div v-else>No existen tareas pendientes</div>
    <br>
    <div v-if="dones.length > 0" class="card">
      <ul class="list-group list-group-flush">
        <li class="list-group-item" v-for="done in dones" :key="done.id">
          {{ done.title }}
          <span>
            <small class="text-muted">
              {{ done.time_since_created }}
            </small>
          </span>
          <span v-if="done.is_done">
            <Done/>
          </span>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import Done from "../components/icons/Done.vue"
import Pending from "../components/icons/Pending.vue"
import TodoForm from "../components/TodoForm.vue"


export default {
  name: "Todos",
  components: {Done, Pending, TodoForm},
  data() {
    return {
      todos: [],
      dones: [],
    };
  },
  methods: {
    markAsDone(todo){
      this.axios.put(`/todos/${todo.id}/`, {
        ...todo,
        is_done:true,
        user:todo.user.id,
      },{headers:{
        Authorization: "Token " + this.token,
      }})
      .then(response => {
        console.log(response)
        this.todos.pop(this.todos.findIndex(_todo => _todo.id == todo.id))
        this.dones.push(response.data)
      })
      .catch(error => console.log(error))
    },
    getTodo() {
      this.axios
        .get("/todos/", {
          headers: {
            Authorization: "Token " + this.token,
          },
        })
        .then((response) => {
          console.log(response);
          this.todos = response.data.filter(data => data.is_done == false);
          this.dones = response.data.filter(data => data.is_done == true);
        })
        .catch((error) => console.log(error));
    },
  },
  computed: {
    token() {
      return this.$store.state.token;
    },
    user() {
      return this.$store.state.user;
    },
  },
  created() {
    this.getTodo();
  },
};
</script>
