<template>
  <img
    :src="'/avatars/' + name"
    :alt="alt"
    class="inline-block object-cover rounded-full mx-2"
    :class="[`w-${size}`, `h-${size}`]"
  />
</template>

<script setup>
defineProps({
  name: {
    type: String,
    required: true
  },
  alt: {
    type: String,
    default: ''
  },
  size: {
    type: String,
    default: '8'
  }
})
</script>
