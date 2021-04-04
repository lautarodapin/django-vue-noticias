import { createStore } from 'vuex'

const WS_URL = process.env.VUE_APP_WS_URL

export default createStore({ 
    state:{
        token: localStorage.getItem("token") || '',
        status: '',
        user:null,
        notas:[],
        ws: null,
        messages: [],
    },
    getters:{
        isLog: state => !!state.token
    },
    mutations:{
        AUTH_REQUEST: state => state.status = 'loading',
        AUTH_SUCCESS: state => state.status = 'success',
        AUTH_ERROR: state => state.status = 'error',
        AUTH_NOT_LOG: state => state.status = 'not log',
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
        },
        addMessage(state, data){
            state.messages.push(data)
        }
    },
    actions:{
        addMessage(context, message){
            context.commit("addMessage", message);
        },
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
        },
        getToken(context, axios){
            console.log("Store get token")
            context.commit("AUTH_REQUEST");
            if (context.state.token != ''){
                axios.post("/get-token/", {
                    token: context.state.token,
                }, {headers:{
                    Authorization: `Token ${context.state.token}`,
                }})
                .then(response => {
                    console.log("Get token", response)
                    context.commit("login", response.data)
                    context.dispatch("setWs")
                    context.commit("AUTH_SUCCESS");
                })
                .catch(error => {
                    console.log(error)
                    context.commit("AUTH_ERROR")
                })
            }
            context.commit("AUTH_NOT_LOG");
        }
    },
})