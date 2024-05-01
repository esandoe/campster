<script setup>
import { RouterView } from 'vue-router'
import Navbar from './components/Navbar.vue'
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
