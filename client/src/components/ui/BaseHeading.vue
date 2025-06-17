<template>
  <h2 :class="headingClass">
    <slot />
  </h2>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'md',
    validator: (v) => ['sm', 'md', 'xl'].includes(v)
  }
})

const headingClass = computed(() => {
  const base = 'font-semibold text-[#08384e]'
  switch (props.variant) {
    case 'xl':
      return `${base} text-6xl font-bold max-w-prose`
    case 'sm':
      return `${base} text-xl`
    case 'md':
    default:
      return `${base} text-3xl py-5`
  }
})
</script>
