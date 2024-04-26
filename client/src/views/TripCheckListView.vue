<template>
  <div class="relative overflow-x-auto shadow-md sm:rounded-lg">
    <table class="table-auto text-sm text-left text-gray-500 rounded-md">
      <thead class="text-xs text-gray-700 uppercase bg-gray-50">
        <tr>
          <th scope="col" class="px-6 py-3">Product</th>
          <th scope="col" class="px-6 py-3">Qty</th>
          <th scope="col" class="px-6 py-3">Packed</th>
          <th scope="col" class="px-6 py-3">Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in items" :key="item.product" class="bg-white border-b hover:bg-gray-50">
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
                  v-bind:value="item.quantity"
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
            <a href="#" class="font-medium text-red-600 hover:underline">Remove</a>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { reactive } from 'vue'
import MinusIcon from '../components/icons/MinusIcon.vue'
import PlusIcon from '../components/icons/PlusIcon.vue'

const items = reactive([
  { product: '12 personers glamping lavvo', quantity: 1, packed: false },
  { product: 'Grytesett, 2L + 1L gryter, 2x tallerken', quantity: 1, packed: false },
  { product: 'Zenbivy sovesystem', quantity: 1, packed: false },
  { product: 'Retro Campingvogn', quantity: 1, packed: false },
  { product: 'Fargerik Hengekøye', quantity: 1, packed: false },
  { product: 'Bærbar Grill', quantity: 1, packed: false },
  { product: 'Utendørs Projektor og Lerret', quantity: 1, packed: false },
  { product: 'Stjernetittende Teleskop', quantity: 1, packed: false },
  { product: 'Sammenleggbar Campingstol', quantity: 1, packed: false },
  { product: 'Varmt Kakaosett', quantity: 1, packed: false },
  { product: 'Vandrestaver', quantity: 1, packed: false },
  { product: 'Vanntett Kart og Kompass', quantity: 1, packed: false },
  { product: 'Fotovennlig Kamera', quantity: 1, packed: false }
])

export default {
  setup() {
    return { items }
  },
  components: { MinusIcon, PlusIcon }
}
</script>
