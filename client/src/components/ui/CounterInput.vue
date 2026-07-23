<template>
  <div>
    <label for="counter-input" class="block mb-1 text-sm font-medium text-gray-900 sr-only"
      >Antall:</label
    >
    <div v-if="props.editable" class="flex items-center gap-1.5 bg-gray-50 border border-gray-200 rounded-full p-[3px]">
      <button
        type="button"
        class="flex-shrink-0 w-[22px] h-[22px] rounded-full bg-white text-gray-900 text-sm font-bold inline-flex items-center justify-center hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200"
        @click="model--"
      >
        −
      </button>
      <input
        v-model.number="model"
        type="text"
        class="w-5 flex-shrink-0 text-gray-900 border-0 bg-transparent text-xs font-bold [font-variant-numeric:tabular-nums] text-center p-0 focus:outline-none focus:ring-0"
      />
      <button
        type="button"
        class="flex-shrink-0 w-[22px] h-[22px] rounded-full bg-white text-gray-900 text-sm font-bold inline-flex items-center justify-center hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200"
        @click="model++"
      >
        +
      </button>
    </div>
    <div v-else class="text-sm font-normal text-gray-900">{{ model }}</div>
  </div>
</template>

<script setup>
const model = defineModel('value')
const props = defineProps({
  editable: {
    type: Boolean,
    default: true
  }
})
</script>
