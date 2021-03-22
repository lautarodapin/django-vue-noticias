<template>
  <div class="container">
    <h3>ToDos de {{ user.username }}</h3>
    <form @submit.prevent="createTodo">
        <div class="form-group row">
        <label for="title" class="col-1 col-form-label">
            ToDo: 
        </label>
        <div class="col">
            <input type="text" v-model="form.title" id="title" class="form-control" placeholder="tarea pendiente">
        </div>
        <div class="col-1">
            <input type="submit" value="Crear" class="btn btn-success">
        </div>
        </div>
    </form>
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
            <Pending />
            <button @click="markAsDone(todo)" class="btn btn-secondary">
              DONE
            </button>
          </span>
        </li>
      </ul>
    </div>
    <div v-else>No existen tareas pendientes</div>
    <br />
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
            <Done />
          </span>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import Done from "../components/icons/Done.vue";
import Pending from "../components/icons/Pending.vue";

export default {
  name: "TodosWS",
  components: { Done, Pending },
  data() {
    return {
      todos: [],
      dones: [],
      form:{
        title:""
      }
    };
  },
  methods: {
    createWs() {
      const self = this;
      this.ws.onmessage = function (e) {
        const response = JSON.parse(e.data);
        console.log("On Message", response);
        switch (response.stream) {
          case "todo":
            switch (response.payload.action) {
              case "list":
                self.todos = response.payload.data.filter(
                  (data) => data.is_done == false
                );
                self.dones = response.payload.data.filter(
                  (data) => data.is_done == true
                );
                break;
              case "update":
                var index;
                index = self.dones.findIndex(
                  (done) => done.id == response.payload.data.id
                );
                if (index >= 0) {
                  if (response.payload.data.is_done){
                    self.dones[index] = response.payload.data;
                  }else{
                    self.dones.pop(index);
                    self.todos.push(response.payload.data)
                  }
                } else {
                  index = self.todos.findIndex(
                    (todo) => todo.id == response.payload.data.id
                  );
                  if (response.payload.data.is_done == true) {
                    self.todos.pop(index);
                    self.dones.push(response.payload.data);
                  } else {
                    self.todos[index] = response.payload.data;
                  }
                }
                break;
              case "create":
                if (response.payload.data.is_done == false){
                  self.todos.push(response.payload.data)
                } else {
                  self.dones.push(response.payload.data)
                }
                break;
              default:
                break;
            }
            break;
          default:
            break;
        }
      };
      this.ws.onclose = function (e) {
        console.log("Websocket se cerro", e);
      };
      this.ws.onerror = function (e) {
        console.log("Websocket se cerro", e);
      };

      this.ws.send(
        JSON.stringify({
          stream: "todo",
          payload: {
            action: "subscribe_todos_in_user",
            request_id: Date.now(),
          },
        })
      );
    },
    getTodos() {
      this.ws.send(
        JSON.stringify({
          stream: "todo",
          payload: {
            action: "list",
            request_id: Date.now(),
          },
        })
      );
    },
    markAsDone(todo) {
      this.ws.send(
        JSON.stringify({
          stream: "todo",
          payload: {
            action: "update",
            pk: todo.id,
            request_id: Date.now(),
            data: {
              ...todo,
              is_done: true,
              user: this.user.id,
            },
          },
        })
      );
    },
    createTodo(){
      this.ws.send(JSON.stringify({
        stream: "todo",
        payload: {
          action: "create",
          request_id: Date.now(),
          data: {
            title: this.form.title,
            user: this.user.id,
          }
        }
      }))
    }
  },
  computed: {
    token() {
      return this.$store.state.token;
    },
    user() {
      return this.$store.state.user;
    },
    ws() {
      return this.$store.state.ws;
    },
  },
  created() {
    this.createWs();
    this.getTodos();
  },
};
</script>
