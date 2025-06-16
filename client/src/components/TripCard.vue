<template>
  <div class="p-6 bg-white border border-gray-200 rounded-lg shadow flex flex-col gap-2">
    <div class="flex items-center justify-between mb-2">
      <h5 class="text-2xl font-bold tracking-tight text-gray-900 dark:text-white">
        {{ trip.name }}
      </h5>
      <span
        v-if="trip.start_date || trip.end_date"
        class="inline-block bg-gray-100 text-gray-600 text-xs font-medium px-2 py-1 rounded text-right whitespace-nowrap"
      >
        <template v-if="trip.start_date">
          {{ formatDate(trip.start_date) }}
        </template>
        <template v-if="trip.end_date">
          <br />
          - {{ formatDate(trip.end_date) }}
        </template>
      </span>
    </div>
    <a href="#" class="block">
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
    </a>
    <RouterLink :to="{ name: 'trip-overview', params: { tripId: trip.id } }">
      <PrimaryButton>
        Gå til side
        <ArrowRightIcon class="text-white ms-2" />
      </PrimaryButton>
    </RouterLink>
  </div>
</template>

<script setup lang="ts">
import ArrowRightIcon from '@/components/icons/ArrowRightIcon.vue'
import MapPinAltIcon from '@/components/icons/MapPinAltIcon.vue'
import PrimaryButton from '@/components/ui/PrimaryButton.vue'
import UserGroupIcon from '@/components/icons/UserGroupIcon.vue'
import { pluralize } from '@/components/utils'
import { RouterLink } from 'vue-router'
import SecondaryButton from './ui/SecondaryButton.vue'

interface TripParticipant {
  id: number
  user_id: number
  username: string
  avatar: string
}

defineProps<{
  trip: {
    id: number
    name: string
    start_date?: string | null
    end_date?: string | null
    location?: string | null
    participants: TripParticipant[]
  }
}>()

function formatDate(dateStr?: string | null) {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleDateString(undefined, {
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  })
}
</script>
