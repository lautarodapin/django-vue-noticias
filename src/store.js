import { createStore } from 'vuex'

export default createStore({ 
    state:{
        name: "Vuasdsadsae",
        token: localStorage.getItem("token") || null,
        user:null,
        notas:[],
    },
    getters:{
        isLog: state => state.token && state.user
    },
    mutations:{
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