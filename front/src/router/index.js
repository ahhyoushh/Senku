import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/Login.vue'),
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('../views/Dashboard.vue'),
    },
    {
      path: '/centers/login',
      name: 'center-login',
      component: () => import('../views/CenterLogin.vue'),
    },
    {
      path: '/centers/verify/:token',
      name: 'verify',
      component: () => import('../views/Verify.vue'),
    },
    {
      path: '/centers/dashboard',
      name: 'center-dashboard',
      component: () => import('../views/CenterDashboard.vue'),
    }
  ],
})

export default router
