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
          <PrimaryButton @click="joinTrip()">
            Bli med!
            <ArrowRightIcon />
          </PrimaryButton>
        </div>
      </div>
      <dl class="grid grid-cols-2 gap-3 p-4 mx-auto">
        <div class="grid grid-cols-1">
          <div class="flex justify-between items-center mb-3">
            <h3 class="text-xl font-semibold text-gray-900">Turdetaljer</h3>
            <SecondaryButton
              v-if="!isEditing"
              @click="startEditing"
            >
              ✏️ Rediger
            </SecondaryButton>
            <div v-else class="flex gap-2">
              <PrimaryButton
                @click="saveAllChanges"
              >
                💾 Lagre
              </PrimaryButton>
              <SecondaryButton
                @click="cancelEditing"
              >
                ✕ Avbryt
              </SecondaryButton>
            </div>
          </div>
          <div class="flex flex-col items-left">
            <dt class="text-lg font-semibold text-gray-900">Start-dato</dt>
            <dd v-if="!isEditing" class="mb-2 text-normal">
              {{ startDate }}
            </dd>
            <dd v-else class="mb-2 text-normal">
              <input
                type="date"
                v-model="editedTrip.start_date"
                class="px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm text-gray-900"
              />
            </dd>
          </div>
          <div class="flex flex-col items-left">
            <dt class="text-lg font-semibold text-gray-900">Slutt-dato</dt>
            <dd v-if="!isEditing" class="mb-2 text-normal">
              {{ endDate }}
            </dd>
            <dd v-else>
              <input
                type="date"
                v-model="editedTrip.end_date"
                class="px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm text-gray-900"
              />
            </dd>
          </div>
          <div class="flex flex-col items-left">
            <dt class="text-lg font-semibold text-gray-900">Lokasjon</dt>
            <dd v-if="!isEditing" class="mb-2 text-normal">
              <a :href="`https://maps.google.com/?q=${trip?.location}`" class="text-blue-600 hover:text-blue-800">🧭{{ trip?.location }}</a>
            </dd>
            <dd v-else>
              <TextInput
                v-model="editedTrip.location"
                placeholder="Stedsnavn eller koordinater (f.eks. 60.601625, 7.503549)"
              />
            </dd>
          </div>
        </div>
        <div class="space-y-1 text-gray-500">
          <ParticipantList :participants="participants" />
        </div>
      </dl>
    </div>

    <!-- Weather forecast widget -->
    <div v-if="isCoords(trip?.location)" class="mt-4">
      <h2 class="py-3 text-lg font-semibold text-gray-900">Værmelding</h2>
      <div v-if="weatherLoading" class="text-sm text-gray-400">Henter værmelding…</div>
      <div v-else-if="weatherError" class="text-sm text-gray-400">{{ weatherError }}</div>
      <div v-else-if="weather" class="overflow-x-auto">
        <p class="text-xs text-gray-400 mb-2">
          📍 {{ weather.location.name }} · Kilde:
          <a
            href="https://www.yr.no"
            target="_blank"
            rel="noopener"
            class="underline hover:text-gray-600"
            >YR.no</a
          >
          · Viser kun dager YR.no har prediksjon for (vanligvis maks ~10 dager frem i tid)
        </p>
        <p v-if="weather.forecast.length === 0" class="text-sm text-gray-400 italic">
          {{
            tripInPast
              ? 'Turen er allerede over — YR.no gir ikke værmelding for datoer som har vært.'
              : 'YR.no har ingen værmelding for denne perioden ennå.'
          }}
        </p>
        <div class="flex gap-2 pb-2">
          <div
            v-for="day in filteredForecast"
            :key="day.date"
            class="flex flex-col items-center min-w-[72px] rounded-lg bg-gray-50 border border-gray-200 p-2"
            :class="{ 'border-blue-400 bg-blue-50': isTripDay(day.date) }"
          >
            <span class="text-xs text-gray-500">{{ shortDay(day.date) }}</span>
            <span class="text-2xl my-1">{{ weatherEmoji(day.symbol) }}</span>
            <span class="text-xs font-semibold text-gray-800"
              >{{ day.temp_max }}° / {{ day.temp_min }}°</span
            >
            <span v-if="day.precipitation > 0" class="text-xs text-blue-500"
              >{{ day.precipitation }} mm</span
            >
          </div>
        </div>
      </div>
    </div>

    <h2 class="py-5 text-lg font-semibold text-gray-900">Innlegg</h2>
    <form v-if="isParticipant" @submit.prevent="createAttachment">
      <div class="w-full mb-4 border border-gray-200 rounded-lg">
        <div class="px-4 py-2 bg-white rounded-t-lg">
          <label for="text" class="sr-only">Skriv innlegg</label>
          <textarea
            v-model="attachment.text"
            id="text"
            name="text"
            rows="3"
            class="w-full px-0 sm:text-sm text-gray-900 resize-none border-none focus:ring-0"
            placeholder="Skriv innlegg"
          ></textarea>
        </div>

        <div class="flex items-center justify-between px-3 py-2 border-t bg-gray-50">
          <PrimaryButton type="submit"> Publiser </PrimaryButton>
          <div class="flex ps-0 text-sm space-x-1 rtl:space-x-reverse items-center sm:ps-2">
            {{ attachment.filename }}
            <label
              for="file-upload"
              type="button"
              class="inline-flex justify-center items-center ms-4 p-2 text-gray-500 rounded cursor-pointer hover:text-gray-900 hover:bg-gray-200"
            >
              <input id="file-upload" class="hidden" type="file" v-on:change="uploadFile" />
              <ImageUploadIcon />
              <span class="sr-only">Upload image</span>
            </label>
          </div>
        </div>
      </div>
    </form>
    <div v-for="attachment in sortedAttachments" :key="attachment.id">
      <div class="flex items-start gap-2.5">
        <img
          :src="'/avatars/' + attachment.user.avatar"
          class="object-cover rounded-full h-10 w-10 my-3"
        />
        <div
          class="flex flex-col w-full my-3 mr-5 leading-1.5 p-4 border-gray-200 bg-gray-100 rounded-e-xl rounded-es-xl"
        >
          <div class="flex items-center space-x-2 rtl:space-x-reverse">
            <span class="text-sm font-semibold text-gray-900">{{ attachment.user.name }}</span>
            <span class="text-sm font-normal text-gray-500">{{
              no_format_date(attachment.created_at, false, true)
            }}</span>
            <span class="grow">&nbsp;</span>
            <button
              type="button"
              class="h-8 w-8 bg-gray-100 text-gray-400 hover:text-gray-900 rounded-lg focus:ring-2 focus:ring-gray-300 p-1.5 hover:bg-gray-200 inline-flex items-center justify-center"
              aria-label="Delete"
              @click="deleteAttachment(attachment.id)"
            >
              <span class="sr-only">Delete</span>
              <CloseIcon />
            </button>
          </div>
          <p class="text-base">{{ attachment.text }}</p>
          <p v-if="attachment.filename" class="text-sm font-normal pb-2.5 text-gray-900">
            <a
              :href="attachment.filepath"
              class="text-blue-700 underline hover:no-underline font-medium break-all"
              >{{ attachment.filepath }}</a
            >
            <img :src="attachment.filepath" class="rounded-lg my-2 max-w-md" />
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import ArrowRightIcon from '@/components/icons/ArrowRightIcon.vue'
import ParticipantList from '@/components/ParticipantList.vue'
import { useAuth } from '@/composables/auth'
import { computed, inject, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import ImageUploadIcon from '@/components/icons/ImageUploadIcon.vue'
import CloseIcon from '@/components/icons/CloseIcon.vue'
import PrimaryButton from '@/components/ui/PrimaryButton.vue'
import SecondaryButton from '@/components/ui/SecondaryButton.vue'
import TextInput from '@/components/ui/TextInput.vue'

const { currentUser } = useAuth()

const tripId = useRoute().params.tripId

const participants = inject('tripParticipants', ref(null))
const trip = ref(null)
const attachments = ref([])
const sortedAttachments = computed(() => {
  const copy = [...attachments.value]
  return copy.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
})

const attachment = ref({
  text: '',
  filename: ''
})

const weather = ref(null)
const weatherLoading = ref(false)
const weatherError = ref(null)

const SYMBOL_EMOJI = {
  clearsky: '☀️',
  fair: '🌤️',
  partlycloudy: '⛅',
  cloudy: '☁️',
  fog: '🌫️',
  lightrain: '🌦️',
  rain: '🌧️',
  heavyrain: '🌧️',
  lightrainshowers: '🌦️',
  rainshowers: '🌧️',
  heavyrainshowers: '🌧️',
  lightsleet: '🌨️',
  sleet: '🌨️',
  heavysleet: '🌨️',
  lightsleetshowers: '🌨️',
  sleetshowers: '🌨️',
  heavysleetshowers: '🌨️',
  lightsnow: '❄️',
  snow: '❄️',
  heavysnow: '❄️',
  lightsnowshowers: '❄️',
  snowshowers: '❄️',
  heavysnowshowers: '❄️',
  thunder: '⛈️',
  lightrainandthunder: '⛈️',
  rainandthunder: '⛈️',
  heavyrainandthunder: '⛈️',
  lightssleetandthunder: '⛈️',
  sleetandthunder: '⛈️',
  lightsnowandthunder: '⛈️',
  snowandthunder: '⛈️',
}

const weatherEmoji = (symbol) => {
  // Strip day/night suffix: "partlycloudy_day" → "partlycloudy"
  const base = symbol?.replace(/_(day|night|polartwilight)$/, '') ?? ''
  return SYMBOL_EMOJI[base] ?? '🌡️'
}

const shortDay = (dateStr) => {
  return new Date(dateStr).toLocaleDateString('NO-no', { weekday: 'short', day: 'numeric', month: 'numeric' })
}

const isTripDay = (dateStr) => {
  if (!trip.value?.start_date || !trip.value?.end_date) return false
  return dateStr >= trip.value.start_date && dateStr <= trip.value.end_date
}

// Local YYYY-MM-DD (not UTC) so the comparison matches end_date's calendar day in Norway
const localToday = () => {
  const now = new Date()
  return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`
}

const tripInPast = computed(() => {
  if (!trip.value?.end_date) return false
  return trip.value.end_date < localToday()
})

const filteredForecast = computed(() => {
  if (!weather.value?.forecast) return []
  if (!trip.value?.start_date) return weather.value.forecast
  // Show up to 3 days before trip start for context, through end date (or 9 days max)
  return weather.value.forecast
})

const isEditing = ref(false)
const editedTrip = ref({ start_date: '', end_date: '', location: '' })

const isCoords = (location) => {
  if (!location) return false
  const parts = location.split(',')
  if (parts.length < 2) return false
  return !isNaN(parseFloat(parts[0])) && !isNaN(parseFloat(parts[1]))
}

const isParticipant = computed(() =>
  participants.value?.some((p) => p.user_id == currentUser.value?.id)
)

const uploadFile = async (event) => {
  attachment.value.filename = event.target.files[0].name
  const formData = new FormData()
  formData.append('file', event.target.files[0])
  const response = await fetch(`/api/trips/${tripId}/attachments/upload-file/`, {
    method: 'POST',
    body: formData
  })
  attachment.value.filename = await response.json()
}

const createAttachment = async () => {
  const response = await fetch(`/api/trips/${tripId}/attachments/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(attachment.value)
  })
  attachments.value.push(await response.json())
  attachment.value.text = ''
  attachment.value.filename = ''
}

const deleteAttachment = async (attachmentId) => {
  if (!confirm('Slette innlegg?')) return

  const response = await fetch(`/api/trips/${tripId}/attachments/${attachmentId}`, {
    method: 'DELETE'
  })
  if (response.ok) {
    attachments.value = attachments.value.filter((at) => at.id != attachmentId)
  } else {
    console.error(`${response.status}, ${response.statusText}: ${await response.text()}`)
  }
}

const no_format_date = (date, include_weekday = false, include_time = false) => {
  return new Date(date).toLocaleDateString('NO-no', {
    weekday: include_weekday ? 'long' : undefined,
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: include_time ? 'numeric' : undefined,
    minute: include_time ? 'numeric' : undefined
  })
}

const startDate = computed(() => {
  return no_format_date(trip.value?.start_date, true)
})

const endDate = computed(() => {
  return no_format_date(trip.value?.end_date, true)
})

const startEditing = () => {
  isEditing.value = true
  editedTrip.value = {
    start_date: trip.value.start_date,
    end_date: trip.value.end_date,
    location: trip.value.location,
  }
}

const cancelEditing = () => {
  isEditing.value = false
  editedTrip.value = { start_date: '', end_date: '', location: '' }
}

const fetchWeather = async () => {
  if (!isCoords(trip.value?.location)) return
  weatherLoading.value = true
  weatherError.value = null
  try {
    const weatherResponse = await fetch(`/api/trips/${tripId}/weather`)
    if (weatherResponse.ok) {
      weather.value = await weatherResponse.json()
    } else {
      const err = await weatherResponse.json()
      weatherError.value = err.error ?? 'Kunne ikke hente værmelding'
    }
  } catch {
    weatherError.value = 'Kunne ikke hente værmelding'
  } finally {
    weatherLoading.value = false
  }
}

const saveAllChanges = async () => {
  const response = await fetch(`/api/trips/${tripId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(editedTrip.value),
  })
  trip.value = await response.json()
  isEditing.value = false
  await fetchWeather()
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
  const attachmentsResponse = await fetch(`/api/trips/${tripId}/attachments/`)
  attachments.value = await attachmentsResponse.json()

  await fetchWeather()
})
</script>

<style></style>
