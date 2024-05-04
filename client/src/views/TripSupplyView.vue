<template>
  <div>
    <!-- {{ JSON.stringify(supplyList) }} -->
    <ul class="w-full divide-y divide-gray-200">
      <div v-for="supplyTarget in supplyList" :key="supplyTarget.id">
        <li class="pb-3 sm:pb-4">
          <div class="flex items-center space-x-4 rtl:space-x-reverse">
            <div class="flex-1 min-w-0">
              <p class="text-sm font-medium text-gray-900 truncate dark:text-white">
                {{ supplyTarget.name }}
              </p>
              <p class="text-sm text-gray-500 truncate dark:text-gray-400 divide-y divide-none">
                <div v-for="item in supplyTarget.items" :key="item.id" class="px-2">
                  {{ item.name }}: {{ item.quantity }}
                </div>
              </p>
            </div>
            <div class="inline-flex items-center text-base text-gray-900 dark:text-white">
              Mål: <span class="font-semibold mx-4"> {{ supplyTarget.target_quantity }}</span>
            </div>
            
            <div class="inline-flex items-center text-base text-gray-900 dark:text-white">
              Bidrag: <span class="font-semibold mx-4"> {{ supplyTarget.sum }}</span>
            </div>
            <div class="inline-flex space-x-3 w-1/4 items-center text-base text-gray-900 dark:text-white">
              <div></div> <ProgressBar :progress="supplyTarget.progress"/></div>
          </div>
        </li>
      </div>
    </ul>
  </div>
</template>

<script setup>
import ProgressBar from '@/components/ProgressBar.vue';
import {  onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'

const supplyList = ref(null)

onMounted(async () => {
  try {
    const tripId = useRoute().params.tripId
    const response = await fetch(`/api/trip/${tripId}/supply-targets`)

    const supplyListResponse = await response.json()
    supplyList.value = supplyListResponse.map(supply => {
      const sum = supply.items.map(i => i.quantity).reduce((partialSum, q) => partialSum + q, 0)
      return {
        ...supply,
        "sum": sum,
        "progress": (sum/supply.target_quantity * 100).toFixed(2)
      }
    })
  } catch (err) {
    return err
  }
})
</script>
