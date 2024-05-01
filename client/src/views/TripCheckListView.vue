<template>
  <div class="relative overflow-x-auto shadow-md sm:rounded-lg">
    <p v-if="!items"><ListSkeleton /></p>
    <table v-else class="table-fixed text-sm text-left text-gray-500 rounded-md">
      <thead class="text-xs text-gray-700 uppercase bg-gray-200">
        <tr>
          <th class="px-6 py-3 w-full">Product</th>
          <th class="px-6 py-3 whitespace-nowrap">Qty</th>
          <th class="px-6 py-3 whitespace-nowrap">Packed</th>
          <th class="px-6 py-3 whitespace-nowrap">Action</th>
        </tr>
      </thead>
      <TransitionGroup name="checklist" tag="tbody">
        <tr v-for="item in items" :key="item.product" class="border-b checklist-item bg-gray-100">
          <td class="w-full px-2 py-1 font-semibold text-gray-900">
            <input
              class="w-full block px-4 py-2 rounded-md outline-none"
              :class="{
                'bg-transparent hover:bg-white cursor-pointer': !item._status?.editing,
                'bg-white': item._status?.editing
              }"
              v-bind:value="item.product"
              @click="item._status.editing = true"
              @focus="item._status.editing = true"
              @keydown.enter="(event) => editItemName(item, event.target.value)"
              @blur="(event) => editItemName(item, event.target.value)"
            />
          </td>
          <td class="px-6 py-3 whitespace-nowrap">
            <div class="flex items-center">
              <button
                class="inline-flex items-center justify-center p-1 me-3 text-sm font-medium h-6 w-6 text-gray-500 bg-white border border-gray-300 rounded-full focus:outline-none hover:bg-gray-100 focus:ring-4 focus:ring-gray-200"
                type="button"
                @click="item.quantity--"
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
                  v-model="item.quantity"
                  required
                />
              </div>
              <button
                class="inline-flex items-center justify-center h-6 w-6 p-1 ms-3 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-full focus:outline-none hover:bg-gray-100 focus:ring-4 focus:ring-gray-200"
                type="button"
                @click="item.quantity++"
              >
                <span class="sr-only">Quantity button</span>
                <plus-icon />
              </button>
            </div>
          </td>
          <td class="px-6 py-3 whitespace-nowrap">
            <label class="inline-flex items-center cursor-pointer">
              <input type="checkbox" value="" class="sr-only peer" v-bind:checked="item.packed" />
              <div
                class="relative w-11 h-6 bg-gray-200 rounded-full peer peer-focus:ring-4 peer-focus:ring-blue-300 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-0.5 after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"
              ></div>
            </label>
          </td>
          <td class="px-6 py-3 whitespace-nowrap">
            <button
              @click="removeItem(item.product)"
              class="font-medium text-red-600 hover:underline"
            >
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
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import MinusIcon from '../components/icons/MinusIcon.vue'
import PlusIcon from '../components/icons/PlusIcon.vue'
import ListSkeleton from '../components/ListSkeleton.vue'
import { scrollIntoView } from '../components/utils'

const items = ref(null)
const newItemName = ref('')
const addNewRef = ref(null)
const errorMsg = ref(null)

function removeItem(item) {
  items.value = items.value.filter((i) => i.product != item)
}

function addItem(productName) {
  productName = productName.trim()

  if (productName === '') {
    errorMsg.value = 'Kan ikke legge til ingenting!'
    return
  }

  const matchingElement = items.value.find(
    (i) =>
      i.product.localeCompare(productName, undefined, {
        usage: 'search',
        sensitivity: 'base'
      }) == 0
  )
  if (matchingElement) {
    errorMsg.value = 'Dette er allerede i listen!'
    return
  }

  errorMsg.value = null
  items.value.push({ product: productName, quantity: 1, packed: false })
  newItemName.value = ''

  scrollIntoView(addNewRef.value, 50)
}

function editItemName(item, newName) {
  item.product = newName
  item._status.editing = false
}

onMounted(async () => {
  try {
    const response = await fetch('/api/trip')
    const itemList = await response.json()
    items.value = itemList.map((item) => ({
      ...item,
      _status: {
        editing: false
      }
    }))
  } catch (err) {
    return err
  }
})
</script>

<style scoped>
.checklist-item {
  transition: all 0.5s;
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
