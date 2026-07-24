<template>
  <div class="h-1.5 rounded-full bg-gray-100 overflow-hidden">
    <div
      class="h-full rounded-full transition-all"
      :class="fillClass"
      :style="{ width: clampedPercent + '%' }"
    ></div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  percent: {
    type: Number,
    required: true
  },
  variant: {
    type: String,
    default: 'blue'
  }
})

const clampedPercent = computed(() => Math.min(100, Math.max(0, props.percent || 0)))

const fillClass = computed(() => (props.variant === 'green' ? 'bg-green-600' : 'bg-blue-600'))
</script>
