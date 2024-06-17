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
          <button
            type="submit"
            class="inline-flex items-center py-2.5 px-4 text-xs font-medium text-white bg-indigo-700 rounded-lg hover:bg-indigo-900 focus:ring-4 focus:outline-none focus:ring-blue-300"
          >
            Publiser
          </button>
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
          </div>
          <p>{{ attachment.text }}</p>
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
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import ImageUploadIcon from '../components/icons/ImageUploadIcon.vue'

const { currentUser } = useAuth()

const participants = ref(null)
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

const editingStartDate = ref(false)
const editingEndDate = ref(false)
const editingLocation = ref(false)

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
  const attachmentsResponse = await fetch(`/api/trips/${tripId}/attachments/`)
  attachments.value = await attachmentsResponse.json()
  console.log(attachments.value)
})
</script>

<style></style>
