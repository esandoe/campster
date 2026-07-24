<template>
  <div class="relative flex-shrink-0" :style="{ width: size + 'px', height: size + 'px' }">
    <svg :width="size" :height="size" :viewBox="`0 0 ${size} ${size}`" class="-rotate-90">
      <circle
        :cx="center"
        :cy="center"
        :r="radius"
        fill="none"
        stroke="#e5e7eb"
        :stroke-width="stroke"
      />
      <circle
        :cx="center"
        :cy="center"
        :r="radius"
        fill="none"
        :stroke="color"
        :stroke-width="stroke"
        stroke-linecap="round"
        :stroke-dasharray="circumference"
        :stroke-dashoffset="dashOffset"
        class="transition-all"
      />
    </svg>
    <span
      class="absolute inset-0 flex items-center justify-center text-[9px] font-bold text-gray-700"
    >
      {{ Math.round(clampedPercent) }}%
    </span>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  percent: { type: Number, required: true },
  size: { type: Number, default: 36 }
})

const stroke = 4
const center = computed(() => props.size / 2)
const radius = computed(() => props.size / 2 - stroke)
const circumference = computed(() => 2 * Math.PI * radius.value)
const clampedPercent = computed(() => Math.min(100, Math.max(0, props.percent || 0)))
const dashOffset = computed(() => circumference.value * (1 - clampedPercent.value / 100))
const color = computed(() => (clampedPercent.value >= 100 ? '#16a34a' : '#2563eb'))
</script>
