<template>
  <nav class="bg-[#ffcfab] border-gray-200 text-gray-700">
    <div class="max-w-screen-lg flex flex-wrap items-center justify-between mx-auto p-4">
      <a href="/" class="flex items-center space-x-3 rtl:space-x-reverse">
        <img src="@/assets/campster_logo_02.svg" class="h-20 -my-2" alt="Campster Logo" />
        <span class="self-center text-2xl font-semibold whitespace-nowrap">Campster</span>
      </a>
      <button
        type="button"
        class="inline-flex items-center p-2 w-10 h-10 justify-center text-sm rounded-lg md:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200"
        aria-controls="navbar-default"
        aria-expanded="false"
        @click="showMenu = !showMenu"
      >
        <span class="sr-only">Open main menu</span>
        <HamburgerMenuIcon />
      </button>
      <div class="w-full md:block md:w-auto" :class="{ hidden: !showMenu }">
        <ul
          class="font-medium flex flex-col items-center p-4 md:p-0 mt-4 border border-gray-100 bg-[#ffebdd] md:bg-transparent rounded-lg md:flex-row md:space-x-8 rtl:space-x-reverse md:mt-0 md:border-0"
        >
          <li v-if="currentUser">
            <RouterLink :to="{ name: 'settings' }">
              <span class="flex items-center whitespace-nowrap">
                <AvatarImage :name="currentUser.avatar" :alt="currentUser.username" />
                <span>{{ currentUser.username }}</span>
              </span>
            </RouterLink>
          </li>
          <li v-if="currentUser">
            <a
              class="cursor-pointer block py-2 px-3 rounded md:hover:bg-transparent md:border-0 md:hover:text-blue-700 md:p-0"
              @click.prevent="logout()"
            >
              Logg ut
            </a>
          </li>
          <li v-else>
            <RouterLink :to="{ name: 'login' }">
              <a
                class="block py-2 px-3 rounded md:hover:bg-transparent md:border-0 md:hover:text-blue-700 md:p-0"
                >Logg inn</a
              >
            </RouterLink>
          </li>
          <li>
            <RouterLink to="/">
              <a
                class="block py-2 px-3 rounded md:hover:bg-transparent md:border-0 md:hover:text-blue-700 md:p-0"
                >Home</a
              >
            </RouterLink>
          </li>
          <li>
            <RouterLink to="/about">
              <a
                class="block py-2 px-3 rounded md:hover:bg-transparent md:border-0 md:hover:text-blue-700 md:p-0"
                >About</a
              >
            </RouterLink>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'
import HamburgerMenuIcon from './icons/HamburgerMenuIcon.vue'
import AvatarImage from './AvatarImage.vue'
import { useAuth } from '@/composables/auth'

const { currentUser, logout } = useAuth()

const showMenu = ref(false)
</script>
