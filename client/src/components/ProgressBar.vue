<template>
  <div class="w-full bg-gray-200 rounded-lg relative h-6">
    <div class="bg-blue-600 h-6 rounded-lg transition-all duration-200" :style="barWidth">
      <div
        v-if="progressNum >= 40"
        class="absolute h-6 flex items-center text-xs font-medium text-white text-right"
        :style="progressBarTextStyle"
      >
        <span v-if="label">{{ label }}&nbsp;/&nbsp;</span>{{ progress }}%
      </div>
    </div>
    <div
      v-if="progressNum < 40"
      class="absolute inset-0 flex items-center text-xs font-medium text-black"
      :style="progressRightStyle"
    >
      <span v-if="label">{{ label }}&nbsp;/&nbsp;</span>{{ progress }}%
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  label: String,
  progress: String
})

const barWidth = computed(() => `width: ${props.progress > 100 ? 100 : props.progress}%`)
const progressNum = computed(() => Number(props.progress))
const progressBarTextStyle = computed(() => ({
  left: 0,
  width: `${props.progress > 100 ? 100 : props.progress}%`,
  justifyContent: 'center',
  position: 'absolute',
  pointerEvents: 'none'
}))
const progressRightStyle = computed(() => ({
  left: `${props.progress > 100 ? 100 : props.progress}%`,
  paddingLeft: '0.5rem',
  justifyContent: 'left',
  position: 'absolute'
}))
</script>
