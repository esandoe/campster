<template>
  <button
    class="inline-flex items-center justify-center w-full px-4 py-2 rounded bg-gray-200 text-gray-700 font-medium hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-400 focus:ring-offset-2 transition"
    v-bind="$attrs"
    :type="props.type ?? 'button'"
  >
    <slot />
  </button>
</template>

<script setup lang="ts">
const props = defineProps<{
  type?: 'button' | 'submit' | 'reset'
}>()
</script>
