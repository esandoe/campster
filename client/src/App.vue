<script setup>
import { RouterLink, RouterView } from 'vue-router'
import Navbar from './components/Navbar.vue'

import { onMounted } from 'vue'
import { initFlowbite } from 'flowbite'

// initialize components based on data attribute selectors
onMounted(() => {
  initFlowbite()
})
</script>

<template>
  <header>
    <Navbar></Navbar>
  </header>

  <div class="bg-[#d6f0f8] h-screen">
    <RouterView />
  </div>
</template>

<style scoped></style>
