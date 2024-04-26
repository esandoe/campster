<template>
  <div class="container max-w-screen-lg mx-auto py-20">
    <main class="bg-white p-5 rounded-lg shadow">
      <h2 class="text-5xl font-bold text-[#08384e] max-w-prose py-12">Tur til Rustfjellhei</h2>

      <nav class="text-sm font-medium text-center text-gray-500 border-b border-gray-200 mb-4">
        <ul class="flex flex-wrap -mb-px">
          <li class="me-2">
            <RouterLink :to="{ name: 'trip-discussion' }" v-slot="{ isActive }">
              <a
                role="tab"
                :class="
                  isActive
                    ? 'inline-block p-4 border-b-2 text-blue-600 border-blue-600 rounded-t-lg'
                    : 'inline-block p-4 border-b-2 border-transparent rounded-t-lg hover:text-gray-600 hover:border-gray-300'
                "
                >Diskusjon</a
              ></RouterLink
            >
          </li>
          <li class="me-2">
            <RouterLink :to="{ name: 'trip-check-list' }" v-slot="{ isActive }"
              ><a
                role="tab"
                :class="
                  isActive
                    ? 'inline-block p-4 border-b-2 text-blue-600 border-blue-600 rounded-t-lg'
                    : 'inline-block p-4 border-b-2 border-transparent rounded-t-lg hover:text-gray-600 hover:border-gray-300'
                "
                aria-current="page"
                >Pakkelister</a
              ></RouterLink
            >
          </li>
          <li class="me-2">
            <RouterLink :to="{ name: 'trip-settings' }" v-slot="{ isActive }"
              ><a
                role="tab"
                :class="
                  isActive
                    ? 'inline-block p-4 border-b-2 text-blue-600 border-blue-600 rounded-t-lg'
                    : 'inline-block p-4 border-b-2 border-transparent rounded-t-lg hover:text-gray-600 hover:border-gray-300'
                "
                aria-current="page"
                >Innstillinger</a
              ></RouterLink
            >
          </li>
          <li class="me-2">
            <RouterLink :to="{ name: 'trip-members' }" v-slot="{ isActive }"
              ><a
                role="tab"
                :class="
                  isActive
                    ? 'inline-block p-4 border-b-2 text-blue-600 border-blue-600 rounded-t-lg'
                    : 'inline-block p-4 border-b-2 border-transparent rounded-t-lg hover:text-gray-600 hover:border-gray-300'
                "
                aria-current="page"
                >Deltakere</a
              ></RouterLink
            >
          </li>
        </ul>
      </nav>

      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { RouterView, RouterLink } from 'vue-router'
</script>

<style></style>
