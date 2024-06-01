<template>
  <dt class="text-lg font-semibold text-gray-900">Deltakere</dt>
  <span
    v-for="participant in participants"
    :key="participant.id"
    class="flex items-center text-normal"
  >
    <img
      :src="'/avatars/' + participant.avatar"
      class="object-cover rounded-full h-5 w-5 my-1 me-2"
    />
    {{ participant.username }}
  </span>
</template>

<script setup>
defineProps({
  participants: Array
})
</script>
