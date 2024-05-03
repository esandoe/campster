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
          <li v-for="participant in participants" :key="participant.id" class="me-2">
            <RouterLink
              :to="{ name: 'trip-checklist', params: { listId: participant.id } }"
              v-slot="{ isActive }"
              ><a
                role="tab"
                :class="
                  isActive
                    ? 'inline-block p-4 border-b-2 text-blue-600 border-blue-600 rounded-t-lg'
                    : 'inline-block p-4 border-b-2 border-transparent rounded-t-lg hover:text-gray-600 hover:border-gray-300'
                "
                aria-current="page"
                >{{ participant.name }}'s liste</a
              ></RouterLink
            >
          </li>
        </ul>
      </nav>

      <RouterView :key="$route.fullPath" />
    </main>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'

const participants = ref(null)
const trip = ref(null)

const tripId = useRoute().params.tripId

onMounted(async () => {
  const tripResponse = await fetch(`/api/trips/${tripId}`)
  trip.value = await tripResponse.json()
  participants.value = trip.value.participants
})
</script>

<style></style>
