<template>
  <label class="inline-flex items-center cursor-pointer">
    <input
      type="checkbox"
      class="w-5 h-5 text-xl text-blue-600 bg-white border-gray-300 rounded focus:ring-blue-500 focus:ring-2"
      v-model="model"
      />
  </label>
</template>

<script setup>
const model = defineModel()
</script>