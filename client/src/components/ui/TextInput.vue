<template>
  <label
    v-if="name"
    :id="labelId"
    for="email"
    class="block mb-2 text-sm font-medium text-gray-900"
    >{{ name }}</label
  >
  <input
    type="text"
    v-model="model"
    v-bind="$attrs"
    v-bind:aria-describedby="helperTextId"
    class="block w-full p-2.5 text-sm rounded-lg border text-gray-700 bg-gray-100 border-gray-300 focus:ring-blue-500 focus:border-blue-500 disabled:text-gray-500 disabled:bg-gray-200 disabled:cursor-not-allowed"
    :class="{
      'bg-red-50 border-red-500 text-red-900 focus:ring-red-500 focus:border-red-500': !!error
    }"
  />
  <p v-if="description" :id="helperTextId" class="mt-2 text-sm text-gray-500">
    {{ description }}
  </p>

  <p v-if="!!error" class="mt-2 text-sm text-red-600">
    <span class="font-medium">{{ error }}</span>
  </p>
</template>

<script setup>
// Disabled Attribute Inheritance, as we want to set them manually to the input element
defineOptions({
  inheritAttrs: false
})

defineProps({
  name: String,
  description: String,
  error: String
})

const model = defineModel()

const randomId = self.crypto.getRandomValues(new Uint32Array(1))[0]
const helperTextId = 'helper-text-' + randomId
const labelId = 'input-label-' + randomId
</script>
