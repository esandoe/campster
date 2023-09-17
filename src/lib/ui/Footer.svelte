<script lang="ts">
  import {
    Footer,
    FooterCopyright,
    FooterLinkGroup,
    FooterLink,
    Tooltip,
  } from "flowbite-svelte";
  import { GithubSolid } from "flowbite-svelte-icons";
</script>

<Footer>
  <FooterCopyright href="/" by="" year={2023} />
  <FooterLinkGroup
    ulClass="flex flex-wrap items-center mt-3 mr-4 text-sm text-gray-500 dark:text-gray-400 sm:mt-0"
  >
    <FooterLink href="https://github.com/esandoe/campster">
      <GithubSolid />
      <Tooltip placement="bottom">Check out the GitHub</Tooltip>
    </FooterLink>
  </FooterLinkGroup>
</Footer>
