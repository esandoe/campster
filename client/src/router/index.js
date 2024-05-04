import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    component: () => import('../views/AboutView.vue')
  },
  {
    path: '/trip/:tripId',
    name: 'trip',
    component: () => import('../views/TripView.vue'),
    children: [
      {
        path: 'overview',
        name: 'trip-overview',
        component: () => import('../views/TripHomeView.vue')
      },
      {
        path: 'supply-list',
        name: 'trip-supply-list',
        component: () => import('../views/TripSupplyView.vue')
      },
      {
        path: 'checklist/:listId',
        name: 'trip-checklist',
        component: () => import('../views/TripCheckListView.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: routes
})

export default router
