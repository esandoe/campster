<template>
  <div class="relative overflow-x-auto shadow-md sm:rounded-lg">
    <p v-if="!items">
      <ListSkeleton />
    </p>
    <table v-else class="table-fixed text-sm text-left text-gray-500 rounded-md">
      <thead class="text-lg text-gray-700 bg-gray-200">
        <tr>
          <th class="pr-0"></th>
          <th class="px-0 py-3 w-full">Product</th>
          <th class="px-1 md:px-6 py-3 whitespace-nowrap">SupplyTarget</th>
          <th class="px-1 md:px-6 py-3 whitespace-nowrap">Qty</th>
          <th class="px-2 md:px-6 py-3 whitespace-nowrap">Packed</th>
          <th class="px-1 md:px-6 py-3 whitespace-nowrap">Action</th>
        </tr>
      </thead>
      <TransitionGroup name="checklist" tag="tbody">
        <tr
          v-for="(item, pos) in items"
          :key="item.id"
          class="border-b checklist-item"
          :class="{
            'cursor-move bg-gray-200': dragHoverPosition === pos,
            'bg-gray-100': dragHoverPosition !== pos
          }"
          @dragstart="(e) => dragstart_handler(e, pos)"
          @drop="(e) => dropHandler(e, pos)"
          @dragenter.prevent="dragHoverPosition = pos"
          @dragover.prevent
        >
          <td draggable="true" class="cursor-pointer pr-0">
            <DraggableItemIcon />
          </td>
          <td class="w-full px-0 py-1 text-lg text-gray-900">
            <input
              class="w-full block px-4 py-2 rounded-md outline-none"
              :class="{
                'bg-transparent hover:bg-white cursor-pointer': !item._status?.editing,
                'bg-white': item._status?.editing
              }"
              :value="item.name"
              @click="item._status.editing = true"
              @focus="item._status.editing = true"
              @keydown.enter="(event) => editItemName(item, event.target.value)"
              @blur="(event) => editItemName(item, event.target.value)"
            />
          </td>
          <td class="px-1 md:px-6 py-3 whitespace-nowrap">
            <select
              class="block w-full px-4 py-2 text-sm border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
              :value="item.supply_target_id"
              @input="(event) => updateItem(item, 'supply_target_id', event.target.value)"
            >
              <option value="" selected>---</option>
              <option
                v-for="supplyTarget in supplyTargets"
                :key="supplyTarget.id"
                :value="supplyTarget.id"
                @input="editItemSupplyTarget(item, supplyTarget.id)"
              >
                {{ supplyTarget.name }}
              </option>
            </select>
          </td>
          <td class="px-1 md:px-6 py-3 whitespace-nowrap">
            <div class="flex items-center">
              <button
                class="inline-flex items-center justify-center p-1 me-3 text-sm font-medium h-6 w-6 text-gray-500 bg-white border border-gray-300 rounded-full focus:outline-none hover:bg-gray-100 focus:ring-4 focus:ring-gray-200"
                type="button"
                @click="updateItem(item, 'quantity', --item.quantity)"
              >
                <span class="sr-only">Quantity button</span>
                <minus-icon />
              </button>
              <div>
                <input
                  type="number"
                  id="first_product"
                  class="bg-gray-50 w-14 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block px-2.5 py-1"
                  placeholder="0"
                  :value="item.quantity"
                  @input="(event) => updateItem(item, 'quantity', event.target.value)"
                  required
                />
              </div>
              <button
                class="inline-flex items-center justify-center h-6 w-6 p-1 ms-3 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-full focus:outline-none hover:bg-gray-100 focus:ring-4 focus:ring-gray-200"
                type="button"
                @click="updateItem(item, 'quantity', ++item.quantity)"
              >
                <span class="sr-only">Quantity button</span>
                <plus-icon />
              </button>
            </div>
          </td>
          <td class="px-1 md:px-6 py-3 whitespace-nowrap">
            <label class="inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                class="w-5 h-5 text-xl text-blue-600 bg-white border-gray-300 rounded focus:ring-blue-500 focus:ring-2"
                :checked="item.packed"
                @input="updateItem(item, 'packed', !item.packed)"
              />
            </label>
          </td>
          <td class="px-1 md:px-6 py-3 whitespace-nowrap">
            <button @click="removeItem(item)" class="font-medium text-red-600 hover:underline">
              Fjern
            </button>
          </td>
        </tr>
      </TransitionGroup>
    </table>

    <div class="w-full px-6 py-4 font-semibold bg-gray-100 text-gray-400" ref="addNewRef">
      <label for="add-item" class="mb-2 text-sm font-medium text-gray-900 sr-only dark:text-white"
        >Legg til ny</label
      >
      <div class="relative">
        <input
          type="text"
          id="add-item"
          class="block w-full p-4 text-sm border rounded-lg"
          :class="{
            'text-gray-900  border-gray-300 bg-gray-50 focus:ring-blue-500 focus:border-blue-500':
              !errorMsg,
            'bg-red-50 border-red-500 text-red-900 focus:ring-red-500 dark:bg-gray-700 focus:border-red-500':
              !!errorMsg
          }"
          placeholder="Legg til ny"
          v-model="newItemName"
          @keydown.enter="addItem(newItemName)"
          @keydown.esc="errorMsg = null"
        />
        <button
          @click="addItem(newItemName)"
          class="block text-white absolute end-2.5 bottom-2.5 bg-blue-500 hover:bg-blue-700 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-full text-sm p-2"
        >
          <PlusIcon class="h-4 w-4" />
        </button>
      </div>
      <p class="mt-2 text-sm text-red-600 dark:text-red-500">
        <span class="font-medium">{{ errorMsg }}</span>
      </p>
      <button
        class="block text-white bg-blue-500 hover:bg-blue-700 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-full text-sm p-2"
        @click="suggestItemName()"
      >
        ✨ Hva med... ✨
      </button>
    </div>
  </div>
</template>

<script setup>
import ListSkeleton from '@/components/ListSkeleton.vue'
import DraggableItemIcon from '@/components/icons/DraggableItemIcon.vue'
import MinusIcon from '@/components/icons/MinusIcon.vue'
import PlusIcon from '@/components/icons/PlusIcon.vue'
import { scrollIntoView } from '@/components/utils'
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'

const items = ref(null)
const supplyTargets = ref(null)
const newItemName = ref('')
const addNewRef = ref(null)
const errorMsg = ref(null)
const dragHoverPosition = ref(null)
const remainingSuggestions = ref(null)

const params = useRoute().params

const suggestItemName = () => {
  newItemName.value = remainingSuggestions.value.pop() ?? '...godt humør?'
}

Array.prototype.move = function (from, to) {
  this.splice(to, 0, this.splice(from, 1)[0])
  return this
}

function dragstart_handler(event, startPos) {
  event.dataTransfer.setData('startPos', startPos)
  const parentRow = event.target.parentElement
  event.dataTransfer.setDragImage(parentRow, parentRow.width, parentRow.height)
}

function dropHandler(event, dropPos) {
  event.preventDefault()
  items.value.move(event.dataTransfer.getData('startPos'), dropPos)
  dragHoverPosition.value = null

  const prev = items.value[dropPos - 1]?.index || 0
  const next = items.value[dropPos + 1]?.index || 1_000_000_000

  const newIndex = Math.floor((prev + next) / 2)

  updateItem(items.value[dropPos], 'index', newIndex)
}

async function removeItem(item) {
  const response = await fetch(`/api/participant/${params.listId}/items/${item.id}`, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json'
    }
  })

  if (response.ok) items.value = items.value.filter((i) => i.id != item.id)
}

async function addItem(itemName) {
  itemName = itemName.trim()

  if (itemName === '') {
    errorMsg.value = 'Kan ikke legge til ingenting!'
    return
  }

  const matchingElement = items.value.find(
    (i) =>
      i.name.localeCompare(itemName, undefined, {
        usage: 'search',
        sensitivity: 'base'
      }) == 0
  )
  if (matchingElement) {
    errorMsg.value = 'Dette er allerede i listen!'
    return
  }

  errorMsg.value = null
  const response = await fetch(`/api/participant/${params.listId}/items`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ name: itemName })
  })
  const item = await response.json()
  console.log(item)
  items.value.push(item)
  newItemName.value = ''

  scrollIntoView(addNewRef.value, 50)
}

function editItemSupplyTarget(item, supplyTargetId) {
  updateItem(item, 'supply_target_id', supplyTargetId)
}

function editItemName(item, newName) {
  if (item._status?.editing) {
    updateItem(item, 'name', newName)
    item._status.editing = false
  }
}

async function updateItem(item, attr, val) {
  try {
    const response = await fetch(`/api/participant/${params.listId}/items/${item.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ ...item, [attr]: val })
    })
    const savedItem = await response.json()
    item.index = savedItem.index
    item.name = savedItem.name
    item.supply_target_id = savedItem.supply_target_id
    item.quantity = savedItem.quantity
    item.packed = savedItem.packed
  } catch (err) {
    return err
  }
}

onMounted(async () => {
  try {
    const response = await fetch(`/api/trip/${params.tripId}/participant/${params.listId}/items`)
    const itemList = await response.json()
    items.value = itemList
      .map((item) => ({
        ...item,
        _status: {
          editing: false
        }
      }))
      .sort((a, b) => a.index - b.index)
    const supplyResponse = await fetch(`/api/trip/${params.tripId}/supply-targets`)
    supplyTargets.value = await supplyResponse.json()
    const suggestionsResponse = await fetch(`/api/items`)
    const suggestions = await suggestionsResponse.json()
    remainingSuggestions.value = suggestions
    refreshSuggestion()
  } catch (err) {
    return err
  }
})
</script>

<style scoped>
.checklist-move,
.checklist-enter-active,
.checklist-leave-active,
.checklist-item {
  transition:
    all 0.5s ease,
    background-color 0s;
}

.checklist-enter,
.checklist-leave-to {
  opacity: 0;
  transform: translateX(300px);
}

.checklist-leave-active {
  position: absolute;
}
</style>
