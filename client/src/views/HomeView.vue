<template>
  <div class="container max-w-screen-lg mx-auto py-20 shadow-m px-4 lg:px-0">
    <section class="py-12">
      <h2 class="text-6xl font-bold text-[#08384e] max-w-prose">Planlegg tur og del pakkelister</h2>
      <p class="my-4 text-lg font-semibold max-w-prose">
        Campster gjør det enkelt å planlegge felles turer og pakkelister!
      </p>
    </section>

    <section v-if="upcomingTrips.length">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-3xl font-semibold text-[#08384e] py-5">Kommende turer</h2>
        <div v-if="!creatingTrip" class="flex items-center">
          <PrimaryButton @click="tripButtonPress">
            Opprett tur
            <PlusIcon class="text-white mx-2" />
          </PrimaryButton>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 grid-flow-row gap-4">
        <TripCard v-for="trip in upcomingTrips" :key="trip.id" :trip="trip" />
        <div
          v-if="creatingTrip"
          class="p-6 flex flex-col justify-center items-stretch bg-white border border-gray-200 rounded-lg shadow h-full"
        >
          <div class="mb-3">
            <TextInput v-model="tripName" placeholder="Navn på tur" class="mb-2" />
          </div>
          <div class="flex gap-2">
            <PrimaryButton @click="tripButtonPress" class="w-full">Lagre tur</PrimaryButton>
            <TertiaryButton @click="cancelCreateTrip" class="w-full">Avbryt</TertiaryButton>
          </div>
        </div>
      </div>
    </section>
    <section>
      <h2 class="text-3xl font-semibold text-[#08384e] py-5">Nylige turer</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 grid-flow-row gap-4">
        <TripCard v-for="trip in recentTrips" :key="trip.id" :trip="trip" />
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
import { onMounted, ref, computed } from 'vue'
import TextInput from '@/components/ui/TextInput.vue'
import TripCard from '@/components/TripCard.vue'
import SecondaryButton from '@/components/ui/SecondaryButton.vue'
import TertiaryButton from '@/components/ui/TertiaryButton.vue'

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

function cancelCreateTrip() {
  creatingTrip.value = false
  tripName.value = ''
}

onMounted(async () => {
  const response = await fetch('api/trips')
  trips.value = await response.json()
})

const today = new Date()
const upcomingTrips = computed(() =>
  (trips.value || []).filter((trip) => !trip.start_date || new Date(trip.start_date) >= today)
)
const recentTrips = computed(() =>
  (trips.value || []).filter((trip) => trip.start_date && new Date(trip.start_date) < today)
)
</script>
