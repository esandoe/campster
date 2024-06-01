<script setup>
import { RouterView } from 'vue-router'
import Navbar from './components/Navbar.vue'
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
      <Navbar></Navbar>
    </header>
    <div class="bg-[#d6f0f8] min-h-screen">
      <RouterView />
    </div>
  </div>
</template>

<style scoped></style>
