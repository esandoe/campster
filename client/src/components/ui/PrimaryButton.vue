<template>
  <button
    class="inline-flex items-center justify-center px-3 py-2 text-sm font-medium text-center rounded-lg text-white bg-indigo-700 hover:bg-indigo-900 focus:ring-4 focus:outline-none focus:ring-blue-300"
    v-bind="$attrs"
    :type="props.type ?? 'button'"
  >
    <slot></slot>
  </button>
</template>

<script setup lang="ts">
const props = defineProps<{
  type?: 'button' | 'submit' | 'reset'
}>()
</script>
