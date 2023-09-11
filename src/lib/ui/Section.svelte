<script lang="ts">
  export let scheme: string = "light";
</script>

<section class={scheme + "-scheme"}>
  <div class="center">
    <slot />
  </div>
</section>

<style>
  section {
    width: 100%;
    padding-block: 75px;
    padding-inline: 8px;
  }

  section.light-scheme {
    background-color: white;
    color: var(--dark);
  }

  section.dark-scheme {
    background-color: var(--dark);
    color: var(--light);
  }

  .center {
    min-width: 320px;
    max-width: 1584px;
    margin-inline: auto;
  }

  @media (min-width: 320px) {
    section {
      padding-inline: 5.625%;
    }
  }
</style>
