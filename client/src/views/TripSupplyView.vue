<template>
  <div>
    <!-- {{ JSON.stringify(supplyList) }} -->
    <ul class="w-full divide-y divide-gray-200">
      <div v-for="supplyTarget in supplyList" :key="supplyTarget.id">
        <li class="pb-3 sm:pb-4">
          <div class="flex items-center space-x-4 rtl:space-x-reverse">
            <div class="flex-1 min-w-0">
              <p class="text-sm font-medium text-gray-900 truncate">
                {{ supplyTarget.name }}
              </p>
              <div class="text-sm text-gray-500 truncate divide-y divide-none">
                <div v-for="item in supplyTarget.items" :key="item.id" class="px-2">
                  {{ item.name }}: {{ item.quantity }}
                </div>
              </div>
            </div>
            <div class="inline-flex items-center text-base text-gray-900">
              Mål: <span class="font-semibold mx-4"> {{ supplyTarget.target_quantity }}</span>
            </div>

            <div class="inline-flex items-center text-base text-gray-900">
              Bidrag: <span class="font-semibold mx-4"> {{ supplyTarget.sum }}</span>
            </div>
            <div class="inline-flex space-x-3 w-1/4 items-center text-base text-gray-900">
              <ProgressBar :progress="supplyTarget.progress" />
            </div>
            <div class="inline-flex items-center text-base text-gray-900">
              <button
                @click="removeSupplyTarget(supplyTarget)"
                class="font-medium text-red-600 hover:underline"
              >
                Fjern
              </button>
            </div>
          </div>
        </li>
      </div>
      <div ref="addNewRef" class="w-full px-6 py-4 font-semibold bg-gray-100 text-gray-400">
        <label for="add-item" class="mb-2 text-sm font-medium text-gray-900 sr-only"
          >Legg til ny</label
        >
        <div class="flex space-x-2">
          <div class="inline-block w-2/3">
            <TextInput
              type="text"
              id="add-item-name"
              class="bg-white !py-2"
              placeholder="Legg til ny"
            />
          </div>
          <input
            type="number"
            min="1"
            id="add-item-target"
            class="px-3 py-2 w-1/6 border border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm text-gray-900"
            placeholder="Mål"
          />
          <PrimaryButton @click="addSupplyTarget" class="w-1/6"> Legg til </PrimaryButton>
        </div>
      </div>
    </ul>
  </div>
</template>

<script setup>
import ProgressBar from '@/components/ProgressBar.vue'
import PrimaryButton from '@/components/ui/PrimaryButton.vue'
import TextInput from '@/components/ui/TextInput.vue'
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'

const supplyList = ref(null)
const tripId = useRoute().params.tripId

async function addSupplyTarget() {
  const response = await fetch(`/api/trip/${tripId}/supply-targets`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      name: document.getElementById('add-item-name').value,
      target_quantity: document.getElementById('add-item-target').value
    })
  })

  if (response.ok) {
    const supplyTarget = await response.json()
    supplyList.value = [...supplyList.value, supplyTarget]
  }
}

async function removeSupplyTarget(supplyTarget) {
  const response = await fetch(`/api/trip/${tripId}/supply-targets/${supplyTarget.id}`, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ id: supplyTarget.id })
  })

  if (response.ok) {
    supplyList.value = supplyList.value.filter((supply) => supply.id !== supplyTarget.id)
  }
}

onMounted(async () => {
  try {
    const response = await fetch(`/api/trip/${tripId}/supply-targets`)

    const supplyListResponse = await response.json()
    supplyList.value = supplyListResponse.map((supply) => {
      const sum = supply.items.map((i) => i.quantity).reduce((partialSum, q) => partialSum + q, 0)
      return {
        ...supply,
        sum: sum,
        progress: ((sum / supply.target_quantity) * 100).toFixed(2)
      }
    })
  } catch (err) {
    return err
  }
})
</script>
