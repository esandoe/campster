<template>
  <div>
    <div aria-labelledby="trip-attributes">
      <div
        v-if="!isParticipant"
        class="flex flex-col justify-between w-full p-4 rounded-lg shadow-sm md:flex-row bg-gray-50"
      >
        <div class="mb-4 md:mb-0 md:me-4">
          <p class="flex h-full items-center text-sm font-normal text-gray-500">
            Du er ikke deltaker på denne turen enda — bli med da vell!
          </p>
        </div>
        <div class="flex items-center flex-shrink-0">
          <button
            @click="joinTrip()"
            class="inline-flex items-center justify-center px-3 py-2 me-2 text-xs font-medium text-white bg-blue-700 rounded-lg hover:bg-blue-800 focus:ring-4 focus:ring-blue-300"
          >
            Bli med!
            <ArrowRightIcon />
          </button>
        </div>
      </div>
      <dl class="grid grid-cols-2 gap-3 p-4 mx-auto">
        <div class="grid grid-cols-1">
          <div class="flex flex-col items-left">
            <dt class="text-lg font-semibold text-gray-900">Start-dato</dt>
            <dd v-if="!editingStartDate" class="mb-2 text-normal">
              {{ startDate }} <button @click="editingStartDate = true">🧨juster</button>
            </dd>
            <dd v-else class="mb-2 text-normal">
              <input
                type="date"
                v-model="trip.start_date"
                class="px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm text-gray-900"
              />
              <button @click="updateTrip('start_date', trip.start_date)">🗡lagre</button>
            </dd>
          </div>
          <div class="flex flex-col items-left">
            <dt class="text-lg font-semibold text-gray-900">Slutt-dato</dt>
            <dd v-if="!editingEndDate" class="mb-2 text-normal">
              {{ endDate }} <button @click="editingEndDate = true">🧨juster</button>
            </dd>
            <dd v-else>
              <input
                type="date"
                v-model="trip.end_date"
                class="px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm text-gray-900"
              />
              <button @click="updateTrip('end_date', trip.end_date)">🗡lagre</button>
            </dd>
          </div>
          <div class="flex flex-col items-left">
            <dt class="text-lg font-semibold text-gray-900">Lokasjon:</dt>
            <dd v-if="!editingLocation" class="mb-2 text-normal">
              <a :href="`https://maps.google.com/?q=${trip?.location}`">🧭{{ trip?.location }}</a>
              <button @click="editingLocation = true">🧨juster</button>
            </dd>
            <dd v-else>
              <input
                type="text"
                v-model="trip.location"
                class="px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm text-gray-900"
              />
              <button @click="updateTrip('location', trip.location)">🗡lagre</button>
            </dd>
          </div>
        </div>
        <div class="space-y-1 text-gray-500">
          <ParticipantList :participants="participants" />
        </div>
      </dl>
    </div>

    <h2 class="py-5 text-lg font-semibold text-gray-900">Innlegg</h2>
    <div class="flex items-start gap-2.5">
      <img
        src="https://cdn.myanimelist.net/r/42x62/images/characters/10/358813.webp?s=6e486ee37e8bc8f6ac8143b96142831f"
        class="object-cover rounded-full h-10 w-10 my-3"
      />
      <div
        class="flex flex-col w-full my-3 mr-5 leading-1.5 p-4 border-gray-200 bg-gray-100 rounded-e-xl rounded-es-xl"
      >
        <div class="flex items-center space-x-2 rtl:space-x-reverse">
          <span class="text-sm font-semibold text-gray-900">Rin Shima</span>
          <span class="text-sm font-normal text-gray-500">11:46</span>
        </div>
        <p class="text-sm font-normal py-2.5 text-gray-900">
          Les gjennom fjellvettreglene en siste gang før vi drar ut på tur:
        </p>
        <p class="text-sm font-normal pb-2.5 text-gray-900">
          <a
            href="https://www.dnt.no/fjellvettreglene/"
            class="text-blue-700 underline hover:no-underline font-medium break-all"
            >https://www.dnt.no/fjellvettreglene/</a
          >
          <img
            src="https://www.dnt.no/globalassets/fotoware/2023/12/0323massivfoto_mdalseg_16.jpg?width=1920&format=webp"
            class="rounded-lg my-2 max-w-md"
          />
        </p>
      </div>
    </div>
    <div class="flex items-start gap-2.5">
      <img
        src="https://cdn.myanimelist.net/r/42x62/images/characters/2/366169.webp?s=afe9005b70cf1d0193fcd769e020a317"
        class="object-cover rounded-full h-10 w-10 my-3"
      />
      <div
        class="flex flex-col w-full my-3 mr-5 leading-1.5 p-4 border-gray-200 bg-gray-100 rounded-e-xl rounded-es-xl"
      >
        <div class="flex items-center space-x-2 rtl:space-x-reverse">
          <span class="text-sm font-semibold text-gray-900">Nadeshiko Kagamihara</span>
          <span class="text-sm font-normal text-gray-500">11:50</span>
        </div>
        <p class="text-sm font-normal py-2.5 text-gray-900">
          Fjellvettreglene sjekket! Jeg har også pakket ekstra snacks for alle. 🍙 Kan ikke vente
          med å se stjernene fra Rustfjellhei! ✨
        </p>
      </div>
    </div>
    <div class="flex items-start gap-2.5">
      <AnonymousUserIcon />
      <div
        class="flex flex-col w-full my-3 mr-5 leading-1.5 p-4 border-gray-200 bg-gray-100 rounded-e-xl rounded-es-xl"
      >
        <div class="flex items-center space-x-2 rtl:space-x-reverse">
          <span class="text-sm font-semibold text-gray-900">Aoi Inuyama</span>
          <span class="text-sm font-normal text-gray-500">11:55</span>
        </div>
        <p class="text-sm font-normal py-2.5 text-gray-900">
          Husk å ta med varme klær, folkens! Det blir kjølig om natten. 🧣 Og Nadeshiko, ikke glem
          teltet denne gangen! 😅
        </p>
      </div>
    </div>
    <div class="flex items-start gap-2.5">
      <img
        src="https://cdn.myanimelist.net/r/42x62/images/characters/2/337013.webp?s=e53af3011799a7448ad1804a79bade68"
        class="object-cover rounded-full h-10 w-10 my-3"
      />
      <div
        class="flex flex-col w-full my-3 mr-5 leading-1.5 p-4 border-gray-200 bg-gray-100 rounded-e-xl rounded-es-xl"
      >
        <div class="flex items-center space-x-2 rtl:space-x-reverse">
          <span class="text-sm font-semibold text-gray-900">Chiaki Oogaki</span>
          <span class="text-sm font-normal text-gray-500">12:00</span>
        </div>
        <p class="text-sm font-normal py-2.5 text-gray-900">
          Jeg har dobbeltsjekket utstyret og alt ser bra ut. 🔧 La oss møtes ved inngangen til stien
          kl. 14:00. Eventyret venter! 🏕️
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import AnonymousUserIcon from '@/components/icons/AnonymousUserIcon.vue'
import ArrowRightIcon from '@/components/icons/ArrowRightIcon.vue'
import ParticipantList from '@/components/ParticipantList.vue'
import { useAuth } from '@/composables/auth'
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'

const { currentUser } = useAuth()

const participants = ref(null)
const trip = ref(null)

const editingStartDate = ref(false)
const editingEndDate = ref(false)
const editingLocation = ref(false)

const isParticipant = computed(() =>
  participants.value?.some((p) => p.user_id == currentUser.value?.id)
)

const dateOptions = {
  weekday: 'long',
  year: 'numeric',
  month: 'long',
  day: 'numeric'
}

const startDate = computed(() => {
  return new Date(trip.value?.start_date).toLocaleDateString('NO-no', dateOptions)
})

const endDate = computed(() => {
  return new Date(trip.value?.end_date).toLocaleDateString('NO-no', dateOptions)
})

const tripId = useRoute().params.tripId

const updateTrip = async (attributeName, attributeValue) => {
  const response = await fetch(`/api/trips/${tripId}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      [attributeName]: attributeValue
    })
  })
  trip.value = await response.json()
  switch (attributeName) {
    case 'start_date':
      editingStartDate.value = false
      break
    case 'end_date':
      editingEndDate.value = false
      break
    case 'location':
      editingLocation.value = false
      break
  }
}

const joinTrip = async () => {
  const response = await fetch(`/api/trips/${tripId}/join`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    }
  })
  if (response.ok) participants.value.push(await response.json())
}

onMounted(async () => {
  const tripResponse = await fetch(`/api/trips/${tripId}`)
  trip.value = await tripResponse.json()
  participants.value = trip.value.participants
})
</script>

<style></style>
