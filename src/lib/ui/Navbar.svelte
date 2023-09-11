<script>
  import {
    Navbar,
    NavBrand,
    NavLi,
    NavUl,
    NavHamburger,
  } from "flowbite-svelte";

  import logo from "/src/assets/turlogo_sm.png";
</script>

<Navbar let:hidden let:toggle>
  <NavBrand href="/">
    <img src={logo} class="mr-3 h-8 sm:h-11" alt="Logo" />
    <span
      class="self-center whitespace-nowrap text-xl font-semibold dark:text-white"
      >Ut på tur!</span
    >
  </NavBrand>
  <NavHamburger on:click={toggle} />
  <NavUl {hidden}>
    <NavLi href="/">Home</NavLi>
  </NavUl>
</Navbar>
