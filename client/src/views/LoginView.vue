<template>
  <section class="">
    <div class="flex flex-col items-center justify-center px-6 py-8 mx-auto md:pt-32">
      <a href="/" class="flex items-center space-x-3 rtl:space-x-reverse mb-5">
        <span class="self-center text-3xl whitespace-nowrap">Campster</span>
      </a>
      <div class="w-full bg-white rounded-lg shadow md:mt-0 sm:max-w-md xl:p-0">
        <div class="p-6 space-y-4 md:space-y-6 sm:p-8">
          <h1 class="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl">
            Logg inn på din konto
          </h1>
          <form class="space-y-4 md:space-y-6" action="#">
            <div>
              <label for="username" class="block mb-2 text-sm font-medium text-gray-900"
                >Ditt brukernavn</label
              >
              <input
                id="username"
                type="text"
                v-model="username"
                class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5"
                placeholder="Nadeshiko Kagamihara"
                required
              />
            </div>
            <div>
              <label for="password" class="block mb-2 text-sm font-medium text-gray-900"
                >Passord</label
              >
              <input
                id="password"
                type="password"
                v-model="password"
                placeholder="••••••••"
                class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5"
                required
              />
            </div>
            <div class="flex items-center justify-between">
              <div class="flex items-start">
                <div class="flex items-center h-5">
                  <input
                    v-model="remember"
                    aria-describedby="remember"
                    type="checkbox"
                    class="w-4 h-4 border border-gray-300 rounded bg-gray-50 focus:ring-3 focus:ring-primary-300"
                    required
                  />
                </div>
                <div class="ml-3 text-sm">
                  <label for="remember" class="text-gray-500">Husk meg</label>
                </div>
              </div>
            </div>
            <button
              type="submit"
              @click.prevent="login()"
              class="w-full text-white bg-blue-500 hover:bg-blue-700 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center"
            >
              Logg inn
            </button>
          </form>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const username = ref(null)
const password = ref(null)
const remember = ref(null)

async function login() {
  const response = await fetch('/api/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      username: username.value,
      password: password.value,
      remember: remember.value
    })
  })

  const result = await response.json()
  if (result.Success) router.go(0) // Refresh the page on successfull login
}

onMounted(async () => {
  const response = await fetch('api/profile')
  if (response.ok) router.push({ name: 'home' })
})
</script>
