import { createRouter, createWebHistory } from 'vue-router'
import Notas from '../views/Notas.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import NotaForm from '../views/NotaForm.vue'
import Rooms from '../views/Rooms.vue';
import Room from '../views/Room.vue';
import Todos from '../views/Todos.vue';
import TodosWS from '../views/TodosWS.vue';
import store from "../store.js";

const routes = [
  {
    path: '/',
    name: 'Notas',
    component: Notas,
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    beforeEnter(to, from, next){
      if(store.getters.isLog) return next({name:"Notas"})
      return next();
    },
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    beforeEnter(to, from, next){
      if(store.getters.isLog) return next({name:"Notas"})
      return next();
    },
  },
  {
    path: '/todos',
    name: 'Todos',
    component: Todos,
    beforeEnter(to, from, next){
      if(store.getters.isLog) return next()
      return next({name:'Login'})
    }
  },
  {
    path: '/todos-ws',
    name: 'TodosWS',
    component: TodosWS,
    beforeEnter(to, from, next){
      if(store.getters.isLog) return next()
      return next({name:'Login'})
    }
  },
  {
    path: '/rooms',
    name: 'Rooms',
    component: Rooms,
    beforeEnter(to, from, next){
      if (store.getters.isLog) return next()
      return next({name:"Login"})
    },
    children:[ /* TODO no me funciona el router-view en el componente Rooms */
      {
        path: ':room',
        name: 'Room',
        component: Room,
      },
    ]
  },
  {
    path: '/nota-form',
    name: 'NotaForm',
    component: NotaForm,
    beforeEnter(to, from, next){
      console.log(to, from, next);
      if (store.getters.isLog) return next();
      return next({name:"Login"});
    },
  },
  {
    path: '/403',
    name: '403',
    component: ()=>import(/* webpackChunkName: "about" */ '../views/About.vue')
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
