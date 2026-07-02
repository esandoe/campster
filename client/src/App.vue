<script setup>
import { RouterView } from 'vue-router'
import TheNavbar from './components/TheNavbar.vue'
import { useAuth } from './composables/auth'
import { onMounted } from 'vue'

const { updateUser } = useAuth()

onMounted(async () => {
  await updateUser()
})
</script>

<template>
  <div>
    <header>
      <TheNavbar></TheNavbar>
    </header>
    <div class="bg-[#d6f0f8] min-h-screen">
      <RouterView />
    </div>
  </div>
</template>

<style scoped></style>
