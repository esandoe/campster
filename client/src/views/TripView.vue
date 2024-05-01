<template>
  <div class="container max-w-screen-lg mx-auto py-20">
    <main class="bg-white p-5 rounded-lg shadow">
      <h2 class="text-5xl font-bold text-[#08384e] max-w-prose py-12">Tur til Rustfjellhei</h2>

      <nav class="text-sm font-medium text-center text-gray-500 border-b border-gray-200 mb-4">
        <ul class="flex flex-wrap -mb-px">
          <li class="me-2">
            <RouterLink :to="{ name: 'trip-overview' }" v-slot="{ isActive }">
              <a
                role="tab"
                :class="
                  isActive
                    ? 'inline-block p-4 border-b-2 text-blue-600 border-blue-600 rounded-t-lg'
                    : 'inline-block p-4 border-b-2 border-transparent rounded-t-lg hover:text-gray-600 hover:border-gray-300'
                "
                >Oversikt</a
              ></RouterLink
            >
          </li>
          <li class="me-2">
            <RouterLink
              :to="{ name: 'trip-checklist', params: { listId: 1 } }"
              v-slot="{ isActive }"
              ><a
                role="tab"
                :class="
                  isActive
                    ? 'inline-block p-4 border-b-2 text-blue-600 border-blue-600 rounded-t-lg'
                    : 'inline-block p-4 border-b-2 border-transparent rounded-t-lg hover:text-gray-600 hover:border-gray-300'
                "
                aria-current="page"
                >Shimashimarin's liste</a
              ></RouterLink
            >
          </li>
          <li class="me-2">
            <RouterLink
              :to="{ name: 'trip-checklist', params: { listId: 2 } }"
              v-slot="{ isActive }"
              ><a
                role="tab"
                :class="
                  isActive
                    ? 'inline-block p-4 border-b-2 text-blue-600 border-blue-600 rounded-t-lg'
                    : 'inline-block p-4 border-b-2 border-transparent rounded-t-lg hover:text-gray-600 hover:border-gray-300'
                "
                aria-current="page"
                >Nadeshiko 's liste</a
              ></RouterLink
            >
          </li>
          <li class="me-2">
            <a
              role="tab"
              class="p-4 border-b-2 rounded-t-lg inline-flex items-center justify-center cursor-pointer"
              :class="
                isActive
                  ? 'text-blue-600 border-blue-600 '
                  : 'border-transparent hover:text-gray-600 hover:border-gray-300'
              "
              aria-current="page"
              ><PlusIcon class="mr-1" /><span>Opprett liste</span>
            </a>
          </li>
        </ul>
      </nav>

      <RouterView :key="$route.fullPath" />
    </main>
  </div>
</template>

<script setup>
import PlusIcon from '@/components/icons/PlusIcon.vue'
</script>

<style></style>
