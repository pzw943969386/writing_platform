import { createRouter, createWebHistory } from 'vue-router'
import homeRoute from './home'
import route404 from './404'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [...homeRoute, ...route404]
})

export default router
