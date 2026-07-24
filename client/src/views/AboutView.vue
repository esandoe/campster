<template>
  <div class="container max-w-screen-lg mx-auto py-20 px-4 lg:px-0">
    <section class="py-12">
      <BaseHeading variant="xl">Om Campster</BaseHeading>
      <p class="my-4 text-lg font-semibold max-w-prose">
        Campster er et verktøy for å planlegge turer, særlig med hensyn på pakkelister.
      </p>

      <BaseHeading variant="md">Bakgrunn</BaseHeading>
      <p class="my-4 max-w-prose text-gray-700">
        Campster er et hobbyprosjekt, laget av noen typer som har tenkt litt mye på pakkelister.
        Opprinnelig brukte vi skybaserte regneark (som forsåvidt er en kraftig løsning!), men etter
        et par år undret vi om vi kunne lage en bedre tilpasset opplevelse, for å pakke effektivt
        som gruppe og samtidig minimere sjansen for feil.
      </p>
      <p class="my-4 max-w-prose text-gray-700">
        Vi har ingen åpen innmelding, men om du er motivert nok, er det ikke vanskelig å få tak i en
        av oss for å diskutere saken.
      </p>
      <p class="my-4 max-w-prose text-gray-700">
        Koden kan undersøkes på
        <a
          href="https://github.com/esandoe/campster"
          target="_blank"
          rel="noopener"
          class="font-medium text-[#08384e] hover:text-blue-700 underline"
          >GitHub</a
        >.
      </p>
    </section>
  </div>
</template>

<script setup>
import BaseHeading from '@/components/ui/BaseHeading.vue'
</script>

<style></style>
