<template>
  <div class="container max-w-screen-lg mx-auto py-20 px-4 lg:px-0 flex flex-col space-y-5">
    <div class="w-full p-4 rounded-lg shadow-sm md:flex-row bg-gray-50">
      <h1>Profil-innstillinger</h1>

      <div>
        <hr class="my-3" />
        <label
          for="username-text"
          class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
          >Ditt brukernavn</label
        >
        <input
          type="text"
          id="username-text"
          aria-describedby="username-text-explanation"
          class="bg-gray-100 border border-gray-300 text-gray-700 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
          placeholder="brukernavn"
          :value="currentUser?.username"
          disabled
        />
        <p id="username-textexplanation" class="mt-2 text-sm text-gray-500 dark:text-gray-400">
          Logg inn med dette navnet. Du kan (foreløpig) ikke endre ditt brukernavn.
        </p>
      </div>

      <div>
        <hr class="my-3" />
        <label
          for="avatar-selector"
          class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
          >Avatar</label
        >
        <div class="inline-block p-2 bg-gray-200">
          <img
            v-if="currentUser"
            :src="'/avatars/' + currentUser?.avatar"
            class="object-cover rounded-full mx-2 w-14 h-14"
          />
        </div>

        <p id="avatar-textexplanation" class="mt-2 text-sm text-gray-500 dark:text-gray-400">
          Velg din avatar
        </p>
        <div class="flex bg-gray-100">
          <div class="flex flex-wrap">
            <div v-for="avatar in avatars" :key="avatar" class="inline-block m-3">
              <input
                type="radio"
                :id="avatar"
                name="hosting"
                :value="avatar"
                class="hidden peer"
                v-model="selectedAvatar"
                aria-describedby="avatar-textexplanation"
                required
              />
              <label
                :for="avatar"
                class="inline-flex items-center justify-between p-0 text-gray-500 bg-white border border-2 p-1 border-gray-200 cursor-pointer peer-checked:border-blue-600 peer-checked:text-blue-600 hover:text-gray-600 hover:bg-gray-100"
              >
                <img :src="'/avatars/' + avatar" class="object-cover rounded-full w-12 h-12" />
              </label>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div
      class="flex flex-col justify-between w-full p-4 rounded-lg shadow-sm md:flex-row bg-gray-50"
    >
      <h1>Campster-innstillinger</h1>
    </div>
  </div>
</template>

<script setup>
import { useAuth } from '@/composables/auth'
import { onMounted, ref, watch } from 'vue'

const { currentUser, updateUser } = useAuth()

const selectedAvatar = ref(currentUser.value?.avatar)

watch(currentUser, (newValue) => {
  selectedAvatar.value = newValue?.avatar
})

watch(selectedAvatar, async (newValue, oldValue) => {
  if (oldValue != newValue && oldValue && newValue) {
    const response = await fetch('/api/profile/avatar', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ avatar: newValue })
    })
    if (response.ok) updateUser()
  }
})

const avatars = ref(null)

onMounted(async () => {
  const response = await fetch('/api/list-avatars')
  if (response.ok) avatars.value = await response.json()
})
</script>
