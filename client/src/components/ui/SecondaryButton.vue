<template>
  <button
    class="inline-flex items-center justify-center px-3 py-2 text-sm font-medium text-center rounded-lg text-gray-900 focus:outline-none bg-white border border-gray-200 hover:bg-gray-100 hover:text-indigo-700 focus:z-10 focus:ring-4 focus:ring-gray-200"
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
