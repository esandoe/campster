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
    path: '/trip',
    name: 'trip',
    component: () => import('../views/TripView.vue'),
    children: [
      {
        path: 'discussion',
        name: 'trip-discussion',
        component: () => import('../views/TripDiscussionView.vue')
      },
      {
        path: 'check-list',
        name: 'trip-check-list',
        component: () => import('../views/TripCheckListView.vue')
      },
      {
        path: 'settings',
        name: 'trip-settings',
        component: () => import('../views/TripSettingsView.vue')
      },
      {
        path: 'members',
        name: 'trip-members',
        component: () => import('../views/TripMembersView.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: routes
})

export default router
