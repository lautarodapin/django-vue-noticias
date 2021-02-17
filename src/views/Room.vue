<template>
  <div>
    <h3>{{ room.nombre }} | {{ room.host.username }}</h3>
    <div id="chat">
      <p v-for="(message, index) in messages" :key="index">
        {{ message.created_at_formatted }} | {{ message.user.username }} :
        {{ message.text }}
      </p>
    </div>
    <form action="" method="post">
        <textarea v-model="comentario" rows="3"></textarea>
        <input type="submit" value="Comentar">
    </form>
  </div>
</template>

<script>
export default {
  name: "Room",
  components: {},
  data() {
    return {
      room: Object(),
      messages: [],
      comentario:"",
    };
  },
  methods: {
    getRoom() {
      this.axios
        .get(`/rooms/${this.pk}/`)
        .then((response) => {
          console.log(response);
          this.room = response.data;
          this.messages = response.data.messages;
        });
    },
  },
  computed: {
    pk() {
      return this.$route.params.room;
    },
    token() {
      return this.$store.state.token;
    },
    user() {
      return this.$store.state.user;
    },
  },
  created() {
    this.getRoom();
  },
};
</script>
