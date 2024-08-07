<template>
  <div class="container max-w-screen-lg mx-auto py-20 shadow-m px-4 lg:px-0">
    <section class="py-12">
      <h2 class="text-6xl font-bold text-[#08384e] max-w-prose">Planlegg tur og del pakkelister</h2>
      <p class="my-4 text-lg font-semibold max-w-prose">
        Campster gjør det enkelt å planlegge felles turer og pakkelister!
      </p>
    </section>

    <section>
      <h2 class="text-3xl font-semibold text-[#08384e] py-5">Nylige turer</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 grid-flow-row gap-4">
        <div
          v-for="trip in trips"
          :key="trip.id"
          class="p-6 bg-white border border-gray-200 rounded-lg shadow"
        >
          <a href="#">
            <h5 class="mb-4 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">
              {{ trip.name }}
            </h5>
          </a>

          <div class="flex flex-row space-x-2 py-0">
            <UserGroupIcon />
            <p class="mb-3 font-normal text-gray-400 dark:text-gray-400">
              {{ pluralize(trip.participants.length, 'deltaker', 'deltakere') }}
            </p>
          </div>
          <div class="flex flex-row space-x-2 py-0">
            <MapPinAltIcon />
            <p class="mb-3 font-normal text-gray-400 dark:text-gray-400">
              {{ trip.location ?? 'N/A' }}
            </p>
          </div>
          <RouterLink :to="{ name: 'trip-overview', params: { tripId: trip.id } }">
            <PrimaryButton>
              Gå til side
              <ArrowRightIcon class="text-white ms-2" />
            </PrimaryButton>
          </RouterLink>
        </div>
        <div class="p-6 bg-white border border-gray-200 rounded-lg shadow">
          <a href="#">
            <h5 class="mb-4 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">
              Opprett ny tur
            </h5>
          </a>
          <TextInput
            v-if="creatingTrip"
            v-model="tripName"
            placeholder="Navn på tur"
          />
          <PrimaryButton @click="tripButtonPress">
            <span v-if="!creatingTrip">Opprett tur</span>
            &ZeroWidthSpace;
            <PlusIcon class="text-white mx-2" />
          </PrimaryButton>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import ArrowRightIcon from '@/components/icons/ArrowRightIcon.vue'
import MapPinAltIcon from '@/components/icons/MapPinAltIcon.vue'
import PlusIcon from '@/components/icons/PlusIcon.vue'
import PrimaryButton from '@/components/ui/PrimaryButton.vue'
import UserGroupIcon from '@/components/icons/UserGroupIcon.vue'
import { pluralize } from '@/components/utils'
import { onMounted, ref } from 'vue'
import TextInput from '@/components/ui/TextInput.vue'

const trips = ref(null)
const creatingTrip = ref(false)
const tripName = ref('')

const tripButtonPress = () => {
  if (!creatingTrip.value) {
    creatingTrip.value = true
  } else if (creatingTrip.value) {
    createTrip(tripName.value)
  }
}

const createTrip = async () => {
  const response = await fetch('api/trips', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name: tripName.value })
  })
  trips.value = [...trips.value, await response.json()]
  creatingTrip.value = false
}

onMounted(async () => {
  const response = await fetch('api/trips')
  trips.value = await response.json()
})
</script>
