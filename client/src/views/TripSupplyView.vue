<template>
  <div>
    <table class="w-full text-sm">
      <thead class="text-xs uppercase text-gray-700 bg-gray-50">
        <tr>
          <th class="px-2 py-2 text-left">Navn</th>
          <th class="px-1 md:px-6 py-2 text-right w-min-20 whitespace-nowrap">Mål</th>
          <th class="px-1 md:px-6 py-2 text-center whitespace-nowrap">Bidrag</th>
          <th class="w-20"></th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="supplyTarget in supplyList"
          :key="supplyTarget.id"
          class="border-b border-b-gray-200"
        >
          <td class="align-top py-2">
            <div v-if="supplyTarget._editing" class="flex gap-2">
              <input
                class="w-full py-0 md:py-1 rounded-sm outline-none bg-gray-50 outline-1 outline-gray-400"
                v-model="supplyTarget._editName"
                @keydown.enter="saveSupplyTarget(supplyTarget)"
                @keydown.esc="cancelEditSupplyTarget(supplyTarget)"
                @blur="saveSupplyTarget(supplyTarget)"
                autofocus
              />
            </div>
            <div v-else>
              <input
                class="w-full py-0 md:py-1 rounded-sm outline-none bg-transparent hover:bg-white cursor-pointer"
                :value="supplyTarget.name"
                readonly
                @click="editSupplyTarget(supplyTarget)"
                @focus="editSupplyTarget(supplyTarget)"
              />
            </div>
            <div class="text-xs text-gray-500 truncate divide-y divide-none">
              <div v-for="item in supplyTarget.items" :key="item.id" class="px-2">
                {{ item.name }}: {{ item.quantity }}
              </div>
            </div>
          </td>
          <td class="align-top text-right py-2">
            <div v-if="supplyTarget._editing">
              <input
                type="number"
                min="1"
                class="w-20 py-0 md:py-1 rounded-sm outline-none bg-gray-50 outline-1 outline-gray-400 text-right"
                v-model.number="supplyTarget._editTargetQuantity"
                @keydown.enter="saveSupplyTarget(supplyTarget)"
                @keydown.esc="cancelEditSupplyTarget(supplyTarget)"
                @blur="saveSupplyTarget(supplyTarget)"
              />
            </div>
            <div v-else>
              <input
                class="w-20 py-0 md:py-1 rounded-sm outline-none bg-transparent hover:bg-white cursor-pointer text-right"
                :value="supplyTarget.target_quantity"
                readonly
                @click="editSupplyTarget(supplyTarget)"
                @focus="editSupplyTarget(supplyTarget)"
              />
            </div>
          </td>
          <td class="align-top text-right font-semibold p-2">
            <div class="flex items-center justify-center space-x-2 w-full">
              <span class="md:hidden whitespace-nowrap">
                {{ supplyTarget.sum ?? '0' }} ({{ supplyTarget.progress ?? 0 }}%)</span
              >
              <ProgressBar
                :label="supplyTarget.sum?.toString() ?? '0'"
                :progress="supplyTarget.progress ?? '0'"
                class="hidden md:inline-block min-w-15"
              />
            </div>
          </td>
          <td class="align-top py-2">
            <button
              @click="removeSupplyTarget(supplyTarget)"
              class="font-medium text-red-600 hover:underline"
            >
              Fjern
            </button>
          </td>
        </tr>
      </tbody>
    </table>
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

function editSupplyTarget(supplyTarget) {
  supplyList.value.forEach((st) => {
    if (st !== supplyTarget) st._editing = false
  })
  supplyTarget._editing = true
  supplyTarget._editName = supplyTarget.name
  supplyTarget._editTargetQuantity = supplyTarget.target_quantity
}

function cancelEditSupplyTarget(supplyTarget) {
  supplyTarget._editing = false
}

async function saveSupplyTarget(supplyTarget) {
  const newName = supplyTarget._editName?.trim()
  const newTarget = Number(supplyTarget._editTargetQuantity)
  if ((!newName || newName === supplyTarget.name) && newTarget === supplyTarget.target_quantity) {
    supplyTarget._editing = false
    return
  }
  const body = {}
  if (newName && newName !== supplyTarget.name) body.name = newName
  if (newTarget && newTarget !== supplyTarget.target_quantity) body.target_quantity = newTarget
  const response = await fetch(`/api/trip/${tripId}/supply-targets/${supplyTarget.id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  })
  if (response.ok) {
    const updated = await response.json()
    supplyTarget.name = updated.name
    supplyTarget.target_quantity = updated.target_quantity
    supplyTarget.progress = (((supplyTarget.sum || 0) / updated.target_quantity) * 100).toFixed(0)
  }
  supplyTarget._editing = false
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
        progress: ((sum / supply.target_quantity) * 100).toFixed(0)
      }
    })
  } catch (err) {
    return err
  }
})
</script>
