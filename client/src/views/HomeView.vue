<template>
  <div class="container max-w-screen-md mx-auto py-20 shadow-m">
    <section class="py-12">
      <h2 class="text-6xl font-bold text-[#08384e] max-w-prose">Planlegg tur og del pakkelister</h2>
      <p class="my-4 text-lg font-semibold max-w-prose">
        Campster gjør det enkelt å planlegge felles turer og pakkelister!
      </p>
    </section>

    <section>
      <h2 class="text-3xl font-semibold text-[#08384e] py-5">Nylige turer</h2>
      <div
        v-for="trip in trips"
        :key="trip.id"
        class="max-w-sm p-6 bg-white border border-gray-200 rounded-lg shadow"
      >
        <a href="#">
          <h5 class="mb-4 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">
            {{ trip.name }}
          </h5>
        </a>

        <div class="flex flex-row space-x-2 py-0">
          <UserGroupIcon />
          <p class="mb-3 font-normal text-gray-400 dark:text-gray-400">Deltakere: 5 personer</p>
        </div>
        <div class="flex flex-row space-x-2 py-0">
          <MapPinAltIcon />
          <p class="mb-3 font-normal text-gray-400 dark:text-gray-400">Deltakere: 5 personer</p>
        </div>
        <RouterLink
          :to="{ name: 'trip-overview', params: { tripId: trip.id } }"
          class="inline-flex items-center px-3 py-2 mt-2 text-sm font-medium text-center text-white bg-indigo-700 rounded-lg hover:bg-indigo-900 focus:ring-4 focus:outline-none focus:ring-blue-300"
        >
          Gå til side
          <ArrowRightIcon class="text-white ms-2" />
        </RouterLink>
      </div>
    </section>
  </div>
</template>

<script setup>
import ArrowRightIcon from '@/components/icons/ArrowRightIcon.vue'
import MapPinAltIcon from '@/components/icons/MapPinAltIcon.vue'
import UserGroupIcon from '@/components/icons/UserGroupIcon.vue'
import { onMounted, ref } from 'vue'

const trips = ref(null)

onMounted(async () => {
  const response = await fetch('api/trips')
  trips.value = await response.json()
})
</script>
