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
              >
                <span class="sr-only">Quantity button</span>
                <svg
                  class="w-3 h-3"
                  aria-hidden="true"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 18 2"
                >
                  <path
                    stroke="currentColor"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M1 1h16"
                  />
                </svg>
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
              >
                <span class="sr-only">Quantity button</span>
                <svg
                  class="w-3 h-3"
                  aria-hidden="true"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 18 18"
                >
                  <path
                    stroke="currentColor"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M9 1v16M1 9h16"
                  />
                </svg>
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

<script setup>
const items = [
  { product: '12 personers glamping lavvo', quantity: 1, packed: false },
  { product: 'Grytesett, 2L + 1L gryter, 2x tallerken', quantity: 1, packed: false },
  { product: 'Zenbivy sovesystem', quantity: 1, packed: false }
]
</script>
