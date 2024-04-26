<template>
  <div class="container max-w-screen-md mx-auto py-20">
    <main class="bg-white p-5 rounded-lg shadow">
      <h2 class="text-5xl font-bold text-[#08384e] max-w-prose py-12">Tur til Rustfjellhei</h2>

      <nav class="text-sm font-medium text-center text-gray-500 border-b border-gray-200">
        <ul class="flex flex-wrap -mb-px">
          <li class="me-2">
            <a
              href="#"
              class="inline-block p-4 border-b-2 border-transparent rounded-t-lg hover:text-gray-600 hover:border-gray-300"
              >Diskusjon</a
            >
          </li>
          <li class="me-2">
            <a
              href="#"
              class="inline-block p-4 text-blue-600 border-b-2 border-blue-600 rounded-t-lg active"
              aria-current="page"
              >Pakkelister</a
            >
          </li>
          <li class="me-2">
            <a
              href="#"
              class="inline-block p-4 border-b-2 border-transparent rounded-t-lg hover:text-gray-600 hover:border-gray-300"
              >Innstillinger</a
            >
          </li>
          <li class="me-2">
            <a
              href="#"
              class="inline-block p-4 border-b-2 border-transparent rounded-t-lg hover:text-gray-600 hover:border-gray-300"
              >Deltakere</a
            >
          </li>
        </ul>
      </nav>

      <check-list class="my-12" />
    </main>
  </div>
</template>

<script>
import CheckList from '@/components/CheckList.vue'
export default {
  components: { CheckList }
}
</script>

<style></style>
