<template>
  <div class="container max-w-screen-lg mx-auto py-0 md:py-20">
    <main class="bg-white p-4 md:p-10 rounded-none md:rounded-lg shadow">
      <div>
        <h2
          v-if="!editingName"
          class="text-5xl font-bold text-[#08384e] max-w-prose pb-4"
          @click="startEditingName"
          title="Klikk for å endre navn"
          style="cursor: pointer"
        >
          {{ trip?.name }}
        </h2>
        <div v-else class="flex items-center gap-2 pb-4">
          <TextInput
            v-model="editedName"
            class="text-5xl font-bold text-[#08384e] max-w-prose"
            @keyup.enter="saveName"
            autofocus
          />
          <PrimaryButton @click="saveName"> Lagre </PrimaryButton>
          <SecondaryButton @click="cancelEditingName"> Avbryt </SecondaryButton>
        </div>
      </div>

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
            <RouterLink :to="{ name: 'trip-supply-list' }" v-slot="{ isActive }">
              <a
                role="tab"
                :class="
                  isActive
                    ? 'inline-block p-4 border-b-2 text-blue-600 border-blue-600 rounded-t-lg'
                    : 'inline-block p-4 border-b-2 border-transparent rounded-t-lg hover:text-gray-600 hover:border-gray-300'
                "
                >Forsyningsmål</a
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
                >{{ participant.username }}'s liste</a
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
import TextInput from '@/components/ui/TextInput.vue'
import PrimaryButton from '@/components/ui/PrimaryButton.vue'
import SecondaryButton from '@/components/ui/SecondaryButton.vue'

const participants = ref(null)
const trip = ref(null)
const editingName = ref(false)
const editedName = ref('')
const tripId = useRoute().params.tripId

function startEditingName() {
  editedName.value = trip.value?.name || ''
  editingName.value = true
}

function cancelEditingName() {
  editedName.value = trip.value?.name || '' // revert to original name
  editingName.value = false
}

async function saveName() {
  if (!editedName.value || editedName.value === trip.value?.name) {
    editingName.value = false
    return
  }
  const response = await fetch(`/api/trips/${tripId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name: editedName.value })
  })
  if (response.ok) {
    trip.value = await response.json()
  }
  editingName.value = false
}

onMounted(async () => {
  const tripResponse = await fetch(`/api/trips/${tripId}`)
  trip.value = await tripResponse.json()
  participants.value = trip.value.participants
})
</script>

<style></style>
