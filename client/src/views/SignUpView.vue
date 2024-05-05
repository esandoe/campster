<template>
  <section class="">
    <div class="flex flex-col items-center justify-center px-6 py-8 mx-auto md:pt-32">
      <a href="/" class="flex items-center space-x-3 rtl:space-x-reverse mb-5">
        <img src="@/assets/logo_sm.png" class="h-10" alt="Campster Logo" />
        <span class="self-center text-3xl whitespace-nowrap">Campster</span>
      </a>
      <div class="w-full bg-white rounded-lg shadow md:mt-0 sm:max-w-md xl:p-0">
        <div class="p-6 space-y-4 md:space-y-6 sm:p-8">
          <h1 class="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl">
            Opprett din profil
          </h1>
          <form class="space-y-4 md:space-y-6" action="#">
            <div>
              <label for="email" class="block mb-2 text-sm font-medium text-gray-900"
                >Din e-post</label
              >
              <input
                type="email"
                v-model="email"
                class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5"
                placeholder="name@company.com"
                required
              />
            </div>
            <div>
              <label for="email" class="block mb-2 text-sm font-medium text-gray-900"
                >Kallenavn</label
              >
              <input
                type="text"
                v-model="name"
                class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5"
                placeholder="name@company.com"
                required
              />
            </div>
            <div>
              <label for="password" class="block mb-2 text-sm font-medium text-gray-900"
                >Passord</label
              >
              <input
                type="password"
                v-model="password"
                placeholder="••••••••"
                class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5"
                required
              />
            </div>
            <div>
              <label for="password" class="block mb-2 text-sm font-medium text-gray-900"
                >Gjenta passord</label
              >
              <input
                type="password"
                v-model="password_repeat"
                placeholder="••••••••"
                class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5"
                required
              />
            </div>

            <button
              @click.prevent="signup()"
              class="w-full text-white bg-blue-500 hover:bg-blue-700 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center"
            >
              Opprett profil
            </button>
          </form>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const email = ref(null)
const name = ref(null)
const password = ref(null)
const password_repeat = ref(null)

async function signup() {
  if (password.value != password_repeat.value) return

  const response = await fetch('/api/signup', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      email: email.value,
      name: name.value,
      password: password.value
    })
  })

  const result = await response.json()
  if (result.Success) router.push({ name: 'login' })
}
</script>
