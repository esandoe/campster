<template>
  <div
    class="section-box relative rounded-xl border"
    :class="pinned ? 'border-blue-200 bg-blue-50' : 'border-gray-200 bg-white'"
  >
    <div v-if="$slots.header" class="px-4 pt-4 pb-2">
      <slot name="header" />
    </div>
    <slot />
    <slot name="overlay" />
  </div>
</template>

<script setup>
defineProps({
  pinned: { type: Boolean, default: false }
})
</script>
