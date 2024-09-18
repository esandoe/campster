<template>
  <div>
    <label for="counter-input" class="block mb-1 text-sm font-medium text-gray-900 sr-only"
      >Antall:</label
    >
    <div v-if="props.editable" class="relative flex items-center">
      <button
        type="button"
        class="flex-shrink-0 bg-gray-100 hover:bg-gray-200 inline-flex items-center justify-center border border-gray-300 rounded-md h-5 w-5 focus:ring-gray-100 focus:ring-2 focus:outline-none"
        @click="model--"
      >
        <MinusIcon />
      </button>
      <input
        v-model.number="model"
        type="text"
        class="flex-shrink-0 text-gray-900 border-0 bg-transparent text-sm font-normal focus:outline-none focus:ring-0 max-w-[2.5rem] text-center"
        pattern="[0-9]{2}"
        value="12"
      />
      <button
        type="button"
        class="flex-shrink-0 bg-gray-100 hover:bg-gray-200 inline-flex items-center justify-center border border-gray-300 rounded-md h-5 w-5 focus:ring-gray-100 focus:ring-2 focus:outline-none"
        @click="model++"
      >
        <PlusIcon />
      </button>
    </div>
    <div v-else class="text-sm font-normal text-gray-900">{{ model }}</div>
  </div>
</template>

<script setup>
import MinusIcon from '../icons/MinusIcon.vue'
import PlusIcon from '../icons/PlusIcon.vue'

const model = defineModel('value')
const props = defineProps({
  editable: {
    type: Boolean,
    default: true
  }
})
</script>
