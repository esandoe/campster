<template>
  <div>
    <h2 class="py-5 text-lg font-semibold text-gray-900">Deltakere:</h2>
    <ul class="space-y-1 text-gray-500 list-inside">
      <li v-for="participant in participants" :key="participant.id" class="flex items-center ps-2">
        <img
          :src="'/avatars/' + participant.avatar"
          class="object-cover rounded-full h-5 w-5 my-1 me-1"
        />
        {{ participant.name }}
      </li>
    </ul>

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
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'

const tripId = useRoute().params.tripId

const participants = ref(null)

onMounted(async () => {
  const response = await fetch(`/api/trip/${tripId}/participants`)
  participants.value = await response.json()
})
</script>

<style></style>
