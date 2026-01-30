<template>
  <div class="container max-w-screen-lg mx-auto py-20 px-4 lg:px-0 flex flex-col space-y-5">
    <div class="w-full p-4 rounded-lg shadow-sm md:flex-row bg-gray-50">
      <h1>Profil-innstillinger</h1>
      <hr class="my-3" />

      <div>
        <TextInput
          name="Ditt brukernavn"
          description="Logg inn med dette navnet. Du kan (foreløpig) ikke endre ditt brukernavn."
          placeholder="brukernavn"
          :value="currentUser?.username"
          disabled
        />
      </div>

      <div>
        <hr class="my-3" />
        <label for="avatar-selector" class="block mb-2 text-sm font-medium text-gray-900"
          >Avatar</label
        >
        <div class="inline-block p-2 bg-gray-200">
          <img
            v-if="currentUser"
            :src="'/avatars/' + currentUser?.avatar"
            class="object-cover rounded-full mx-2 w-14 h-14"
          />
        </div>

        <p id="avatar-textexplanation" class="mt-2 text-sm text-gray-500">Velg din avatar</p>
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

    <div v-if="currentUser != null" class="w-1/2 p-4 rounded-lg shadow-sm md:flex-row bg-gray-50">
      <h2>Bytt passord</h2>
      <hr class="my-3" />
      <div
        v-if="currentUser.is_pending"
        class="p-4 mb-4 text-sm text-yellow-800 rounded-lg bg-yellow-50 border border-yellow-300"
        role="alert"
      >
        <strong class="font-bold">Viktig!</strong>
        <p class="mt-1">
          Du må sette et nytt passord før du kan fortsette. Dette er et midlertidig passord som må
          endres.
        </p>
      </div>
      <form id="change-password-form" @submit.prevent="changePassword">
        <div>
          <TextInput name="Gammelt passord" type="password" v-model="oldPassword" required />
        </div>
        <div class="mt-2">
          <TextInput name="Nytt passord" type="password" v-model="newPassword" required />
        </div>
        <div class="mt-2">
          <TextInput
            name="Bekreft nytt passord"
            type="password"
            v-model="confirmNewPassword"
            required
          />
        </div>
        <PrimaryButton type="submit" class="mt-4"> Bytt passord </PrimaryButton>
      </form>
    </div>

    <div
      v-if="currentUser?.is_admin"
      class="w-full p-4 rounded-lg shadow-sm md:flex-row bg-gray-50"
    >
      <h3>Administrer brukere</h3>
      <hr class="my-3" />

      <div class="relative overflow-x-auto shadow-md">
        <table class="w-full text-sm text-left rtl:text-right text-gray-500" v-if="allUsers">
          <thead class="text-xs text-gray-700 uppercase bg-gray-100">
            <tr>
              <th class="px-4 py-2 w-full whitespace-nowrap">Brukernavn</th>
              <th class="px-4 py-2 whitespace-nowrap">Admin</th>
              <th class="px-4 py-2 whitespace-nowrap" colspan="2">Handling</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="user in allUsers"
              :key="user.id"
              class="odd:bg-white odd:even:bg-gray-50 even:border-b"
            >
              <th scope="row" class="px-2 py-2 w-full whitespace-nowrap">
                {{ user.username }}
              </th>
              <td class="px-4 py-2 whitespace-nowrap">
                <input
                  type="checkbox"
                  :checked="user.is_admin"
                  @change="updateUserIsAdmin(user.id, !user.is_admin)"
                />
              </td>
              <td class="px-4 py-2 whitespace-nowrap">
                <a
                  href="#"
                  class="font-medium text-red-600 hover:underline"
                  @click="resetPassword(user.id, user.username)"
                  >Tilbakestill passord</a
                >
              </td>
              <td class="px-4 py-2 whitespace-nowrap">
                <a
                  @click.prevent="deleteUser(user.id)"
                  class="font-medium text-red-600 hover:underline"
                  >Slett</a
                >
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <hr class="mt-5 mb-3" />

      <h4 class="mb-2">Opprett ny bruker</h4>

      <div class="grid grid-cols-1 md:grid-cols-2 md:space-x-5">
        <div>
          <TextInput name="Brukernavn" placeholder="olanordmann" v-model="newUserUsername" />
        </div>

        <div>
          <TextInput
            name="Midlertidig passord"
            type="password"
            placeholder="•••••••••"
            v-model="newUserPassword"
          />
        </div>
      </div>
      <p v-if="addUserErrorMessage" class="mt-2 text-sm text-red-600">
        {{ addUserErrorMessage }}
      </p>
      <PrimaryButton @click.prevent="createUser()" class="mt-4">Opprett bruker</PrimaryButton>
    </div>

    <div
      v-if="currentUser?.is_admin"
      class="w-full p-4 rounded-lg shadow-sm md:flex-row bg-gray-50"
    >
      <h2>Oppdater campster til siste versjon</h2>
      <button
        @click="restartServer()"
        class="mt-4 bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded"
      >
        Oppdater
      </button>
    </div>
  </div>
</template>

<script setup>
import PrimaryButton from '@/components/ui/PrimaryButton.vue'
import TextInput from '@/components/ui/TextInput.vue'
import { useAuth } from '@/composables/auth'
import { onMounted, ref, watch } from 'vue'

const { currentUser, updateUser } = useAuth()

const avatars = ref(null)
const selectedAvatar = ref(currentUser.value?.avatar)
const allUsers = ref(null)

const newUserUsername = ref(null)
const newUserPassword = ref(null)
const addUserErrorMessage = ref(null)

const oldPassword = ref(null)
const newPassword = ref(null)
const confirmNewPassword = ref(null)

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

async function restartServer() {
  fetch('/api/settings/server/update', { method: 'POST' })
}

async function changePassword() {
  if (newPassword.value !== confirmNewPassword.value) {
    alert('Nye passord matcher ikke hverandre')
    return
  }

  fetch('/api/settings/user/change-password', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      old_password: oldPassword.value,
      new_password: newPassword.value,
      confirm_new_password: confirmNewPassword.value
    })
  })
    .then((response) => response.json())
    .then(async (data) => {
      if (data.success) {
        await updateUser()
        alert('Du byttet passord, flott!')
        oldPassword.value = ''
        newPassword.value = ''
        confirmNewPassword.value = ''
      } else {
        alert('Feil: ' + data.Error)
      }
    })
    .catch((error) => {
      console.error('Error:', error)
    })
}

async function createUser() {
  const [username, temp_password] = [newUserUsername.value, newUserPassword.value]
  const response = await fetch(`/api/settings/users`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      username: username,
      temp_password: temp_password
    })
  })

  if (!response.ok) {
    addUserErrorMessage.value = (await response.json()).Error
    return
  }

  addUserErrorMessage.value = null
  newUserUsername.value = null
  newUserPassword.value
  fetchUserList()
}

function fetchUserList() {
  fetch('/api/settings/users')
    .then((result) => result.json())
    .then((value) => (allUsers.value = value))
}

async function deleteUser(userId) {
  const response = await fetch(`/api/settings/users/${userId}`, {
    method: 'DELETE'
  })

  if (response.ok) {
    fetchUserList()
  }
}

async function updateUserIsAdmin(userId, isAdmin) {
  const response = await fetch(`/api/settings/users/${userId}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      is_admin: isAdmin
    })
  })

  if (response.ok) {
    fetchUserList()
  }
}

async function resetPassword(userId, username) {
  const response = await fetch(`/api/settings/users/${userId}/password-reset`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json'
    }
  })

  if (response.ok) {
    const body = await response.json()
    const pass = body['TemporaryPassword']
    alert(`Nytt midlertidig passord for ${username}: ${pass}`)
  } else {
    alert('Feil')
  }
}

onMounted(() => {
  fetch('/api/list-avatars')
    .then((result) => result.json())
    .then((value) => (avatars.value = value))

  fetchUserList()
})
</script>
