<template>
  <div class="container">
    <h3>ToDos de {{ user.username }}</h3>
    <div v-if="todos != null">
      <ul class="list-group">
        <li class="list-group-item" v-for="todo in todos" :key="todo.id">
          {{ todo.title }}
          <span>
            <small class="text-muted">
              {{ todo.time_since_created }}
            </small>
          </span>
          <span v-if="todo.is_done">
            <Done/>
          </span>
          <span v-else>
            <Pending/>
            <button @click="markAsDone(todo)" class="btn btn-sm btn-secondary">
              DONE
            </button>
          </span>
        </li>
      </ul>
    </div>
    <div v-else>No hay todos</div>
  </div>
</template>

<script>
import Done from "../components/icons/Done.vue"
import Pending from "../components/icons/Pending.vue"

export default {
  name: "Todos",
  components: {Done, Pending},
  data() {
    return {
      todos: null,
      dones: null,
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
        this.todos[this.todos.findIndex(_todo => _todo.id == todo.id)] = response.data
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
          this.todos = response.data;
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
