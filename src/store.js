import { createStore } from 'vuex'

const WS_URL = process.env.VUE_APP_WS_URL

export default createStore({ 
    state:{
        name: "Vuasdsadsae",
        token: localStorage.getItem("token") || null,
        user:null,
        notas:[],
        ws: null,
    },
    getters:{
        isLog: state => state.token && state.user
    },
    mutations:{
        setWs(state, ws){
            console.log("Mutation setWs", state, ws);
            state.ws = ws;
        },
        login(state, data){
            console.log("Mutation login executed", data)
            state.token = data.token;
            state.user = data.user 
        },
        logout(state){
            console.log("Mutation logout executed")
            state.token = null;
            state.user = null;
            localStorage.removeItem("token");
        },
        setNotas(state, payload){
            state.notas = payload
        }
    },
    actions:{
        setWs(context){
            const ws = new WebSocket(WS_URL +  "/ws/?token=" + context.state.token )
            context.commit("setWs", ws);
        },
        getNotas(context, axios){
            console.log("Store getNotas")
            axios.get("/nota/")
            .then(response=>{
                // this.notas=data.data;
                context.commit("setNotas", response.data)
                console.log(response)
            })
        }
    },
})