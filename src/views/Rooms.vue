<template>
  <div>
    <h3>Ingrese a un chat!</h3>
    <div class="row">
      <div v-for="(room, index) in rooms" :key="index" class="col">
        <div class="card">
          <div class="card-header">
            {{ room.nombre }}  <span class="text-muted"> | Host: {{ room.host.username }} </span>
          </div>
          <div class="card-body">
            <button
              @click="
                this.selected = true;
                this.room = room;
                this.getRoom();
                this.createWs();
              "
              class="btn btn-sm btn-success"
            >
              Entrar
            </button>
            
          </div>
        </div>
        <!-- TODO no funciona el router link -->
        <!-- <router-link :to="{name:'Room', params:{room:room.pk}}">Rooms</router-link> -->
      </div>
    </div>
    <hr />
    <div v-if="selected == false" class="container">
      <h4>Crear nuevo chat</h4>
      <form  @submit.prevent="createRoom" method="post">
        <div class="form-group">
          <label for="id_nombre">Nombre</label>
          <input type="text" class="form-control" name="Nombre" v-model="nombre" id="id_nombre" />
        </div>
        <input type="submit" value="Crear" class="btn btn-sm btn-success"/>
      </form>
    </div>
    <div v-else class="container">
      <floating-button @click.prevent="back"></floating-button>



      <div class="container text-left">
        <div class="row">
            <div class="col-md-9">
                <h3>{{ room.nombre }} | {{ room.host.username }}</h3>
                <div style="overflow-y:scroll;height:20rem;">
                    <div id="messages">
                        <div v-for="(message, index) in messages" :key="index" class="alert alert-info thin-alert" style="padding: .25rem 1.25rem;" role="alert">
                            <small>{{message.created_at_formatted}}  |  </small><strong>{{message.user_extra.username}}</strong>
                            {{message.text}}
                        </div>
                    </div>
                </div>
                <form @submit.prevent="submitMensaje">
                    <div class="form-group row">
                        <label for="chat-input" class="col-sm-1 col-form-label">Message</label>
                        <div class="col-sm-9">
                            <input type="text" class="form-control" id="chat-input" placeholder="Enter message...">
                        </div>
                        <div class="col-sm-2">
                            <button type="submit" class="btn btn-primary">Send</button>
                        </div>
                    </div>
                </form>
            </div>
            <div class="col-md-3">
                <h4>Connected Users</h4>
                <ul id="users">
                    <li v-for="(user, index) in current_users" :key="index">
                        {{user.username}}
                    </li>
                </ul>
            </div>
        </div>
        </div>
        <!-- old -->


<!-- 
      <div class="current-users card">
          <ul class="list-group list-group-flush">
              <li v-for="(user, index) in current_users" :key="index" class="list-group-item">
                  {{user.username}}
              </li>
          </ul>
      </div>
      <div class="row chat m-2" style="overflow-y:scroll; height: 300px">
        <div v-for="(message, index) in messages" :key="index" class="col-12 mb-2">
          <div class="card">
            <div class="card-bod">
              <p class="card-text">
                <small class="text-muted">
                  {{ message.created_at_formatted }} 
                |
                {{ message.user_extra.username }}
                : 
                </small>
                {{ message.text }}
              </p>
            </div>
          </div>
        </div>
        <hr />
      </div>
      <form @submit.prevent="submitMensaje" method="post">
        <div class="form-group">
          <textarea
            name="mensaje"
            id="id_mensaje"
            v-model="mensaje"
            class="form-control"
            rows="3"
          ></textarea>
        </div>
        <input type="submit" value="Enviar" class="btn btn-sm btn-success"/>
      </form> -->
    </div>
    <!-- <router-view></router-view> -->
  </div>
</template>

<script>
import FloatingButton from "../components/FloatingButton.vue";


export default {
  name: "Rooms",
  components: {
    FloatingButton
  },
  data() {
    return {
      nombre: "",
      rooms: [],
      selected: false,
      room: null,
      mensaje: "",
      messages: [],
      current_users:[],
    };
  },
  methods: {
    back(){
      this.selected = false;
      this.leaveRoom();
    },
    submitMensaje() {
       this.ws.send(JSON.stringify({
           stream:"room",
           payload:{
               action:"create_message",
               message:this.mensaje,
               request_id:Date.now(),
           }
       }));
       this.mensaje = ""
    },
    leaveRoom(){
        this.ws.send(JSON.stringify({
            stream:"room",
            payload:{
                action:"leave_room",
                pk:this.room.pk,
                request_id:Date.now(),
            }
        }))
    },
    getRoom() {
      this.axios.get(`/rooms/${this.room.pk}/`).then((response) => {
        console.log(response);
        this.room = response.data;
        this.messages = response.data.messages;
      });
    },
    getRooms() {
      this.axios.get("/rooms/").then((response) => {
        console.log(response);
        this.rooms = response.data;
      });
    },
    createRoom() {
      const data = {
        nombre: this.nombre,
        host: this.user.id,
      };
      this.axios
        .post("/rooms/", data, {
          headers: {
            Authorization: "Token " + this.token,
          },
        })
        .then((response) => {
          console.log(response);
          this.rooms.push(response.data);
        });
    },
    createWs() {
        const component = this;
      this.ws.onmessage = function (e) {
        const response = JSON.parse(e.data);
        console.log("Onmessage", response);
        switch (response.stream) {
            case "room":
                switch (response.payload.action) {
                    case "create":
                        component.messages = [...component.messages, response.payload.data]
                        break;
                    case "update_users":
                        component.current_users = response.payload.data
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
        // setTimeout(this.createWs, 1000*10)
      };
      this.ws.send(
        JSON.stringify({
          stream: "room",
          payload: {
            action: "subscribe_instance",
            pk: this.room.pk,
            request_id: Date.now(),
          },
        })
      );
      this.ws.send(
        JSON.stringify({
          stream: "room",
          payload: {
            action: "subscribe_to_messages_in_room",
            pk: this.room.pk,
            request_id: Date.now(),
          },
        })
      );
      this.ws.send(
        JSON.stringify({
          stream: "room",
          payload: {
            action: "join_room",
            pk: this.room.pk,
            request_id: Date.now(),
          },
        })
      );
    },
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
    this.getRooms();
  },
};
</script>
