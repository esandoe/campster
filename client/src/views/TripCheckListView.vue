<template>
  <div class="relative overflow-x-auto shadow-md sm:rounded-lg">
    <p v-if="!items"><ListSkeleton /></p>
    <table v-else class="table-auto text-sm text-left text-gray-500 rounded-md">
      <thead class="text-xs text-gray-700 uppercase bg-gray-50">
        <tr>
          <th scope="col" class="px-6 py-3">Product</th>
          <th scope="col" class="px-6 py-3">Qty</th>
          <th scope="col" class="px-6 py-3">Packed</th>
          <th scope="col" class="px-6 py-3">Action</th>
        </tr>
      </thead>
      <TransitionGroup name="checklist" tag="tbody">
        <tr
          v-for="item in items"
          :key="item.product"
          class="bg-white border-b hover:bg-gray-50 checklist-item"
        >
          <td class="w-full px-6 py-4 font-semibold text-gray-900">{{ item.product }}</td>
          <td class="px-6 py-4">
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
          <td class="px-6 py-4">
            <label class="inline-flex items-center cursor-pointer">
              <input type="checkbox" value="" class="sr-only peer" v-bind:checked="item.packed" />
              <div
                class="relative w-11 h-6 bg-gray-200 rounded-full peer peer-focus:ring-4 peer-focus:ring-blue-300 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-0.5 after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"
              ></div>
            </label>
          </td>
          <td class="px-6 py-4">
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

    <div class="w-full px-6 py-4 font-semibold text-gray-400">
      <label for="add-item" class="mb-2 text-sm font-medium text-gray-900 sr-only dark:text-white"
        >Legg til ny</label
      >
      <div class="relative">
        <input
          type="text"
          id="add-item"
          class="block w-full p-4 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500"
          placeholder="Legg til ny"
          v-model="newItemName"
        />
        <button
          @click="addItem(newItemName)"
          class="block text-white absolute end-2.5 bottom-2.5 bg-blue-500 hover:bg-blue-700 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-full text-sm p-2"
        >
          <PlusIcon class="h-4 w-4" />
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, TransitionGroup } from 'vue'
import MinusIcon from '../components/icons/MinusIcon.vue'
import PlusIcon from '../components/icons/PlusIcon.vue'
import ListSkeleton from '../components/ListSkeleton.vue'

const items = ref(null)
const newItemName = ref('')

function removeItem(item) {
  items.value = items.value.filter((i) => i.product != item)
}

function addItem(productName) {
  items.value.push({ product: productName, quantity: 1, packed: false })
  newItemName.value = ''
}

onMounted(async () => {
  try {
    const response = await fetch('/api/trip')
    items.value = await response.json()
    console.log(items.value)
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
}
.checklist-leave-active {
  position: absolute;
}
</style>
