<template>
  <div class="container max-w-screen-md mx-auto py-20 shadow-m">
    <section class="py-12">
      <h2 class="text-6xl font-extrabold text-[#08384e] max-w-prose">Lag og del pakkelister</h2>
      <p class="my-4 text-lg max-w-prose">
        Campster gjør det enkelt å samarbeide på felles pakkelister!
      </p>
    </section>

    <CheckList />
  </div>
</template>

<script>
import CheckList from '../components/CheckList.vue'

export default {
  setup() {
    return {}
  },
  components: { CheckList }
}
</script>
