<template>
  <nav class="bg-[#ffcfab] border-gray-200 text-gray-700">
    <div class="max-w-screen-lg flex flex-wrap items-center justify-between mx-auto p-4">
      <a href="/" class="flex items-center space-x-3 rtl:space-x-reverse">
        <img src="@/assets/campster_logo_02.svg" class="h-20 -my-2" alt="Campster Logo" />
        <span class="self-center text-2xl font-semibold whitespace-nowrap">Campster</span>
      </a>
      <button
        data-collapse-toggle="navbar-default"
        type="button"
        class="inline-flex items-center p-2 w-10 h-10 justify-center text-sm rounded-lg md:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200"
        aria-controls="navbar-default"
        aria-expanded="false"
      >
        <span class="sr-only">Open main menu</span>
        <svg
          class="w-5 h-5"
          aria-hidden="true"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 17 14"
        >
          <path
            stroke="currentColor"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M1 1h15M1 7h15M1 13h15"
          />
        </svg>
      </button>
      <div class="hidden w-full md:block md:w-auto" id="navbar-default">
        <ul
          class="font-medium flex flex-col p-4 md:p-0 mt-4 border border-gray-100 rounded-lg md:flex-row md:space-x-8 rtl:space-x-reverse md:mt-0 md:border-0"
        >
          <li v-if="user">
            <span class="py-0 px-2 flex items-center text-white">
              <img
                :src="'/avatars/' + user.avatar"
                class="object-cover rounded-full h-5 w-5 mx-2"
              />
              <span>{{ user.name }}</span>
            </span>
          </li>
          <li v-else>
            <RouterLink :to="{ name: 'login' }">
              <a
                class="block py-2 px-3 rounded md:hover:bg-transparent md:border-0 md:hover:text-blue-700 md:p-0"
                aria-current="page"
                >Logg inn</a
              >
            </RouterLink>
          </li>
          <li>
            <RouterLink to="/">
              <a
                class="block py-2 px-3 rounded md:hover:bg-transparent md:border-0 md:hover:text-blue-700 md:p-0"
                aria-current="page"
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
import { onMounted, ref } from 'vue'

const user = ref(null)

onMounted(async () => {
  const response = await fetch('/api/profile')

  if (response.ok) user.value = await response.json()
})
</script>
