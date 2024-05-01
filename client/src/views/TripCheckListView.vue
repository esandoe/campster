<template>
  <div>
    <TripChecklist />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import TripChecklist from '../components/TripChecklist.vue'

onMounted(async () => {
  try {
    const response = await fetch('/api/trip/<trip_id>/participants')
  } catch (err) {
    return err
  }
})
</script>
