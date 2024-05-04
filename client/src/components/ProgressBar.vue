<template>
  <div class="w-full bg-gray-200 rounded-full">
    <div
      class="bg-blue-600 text-xs font-medium text-blue-100 text-center p-0.5 leading-none rounded-full"
      :style="barWidth"
    >
      {{ progress }}%
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  progress: String
})

const barWidth = computed(() => `width: ${props.progress > 100 ? 100 : props.progress}%`)
</script>
