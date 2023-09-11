<script lang="ts">
  import { Router, Route } from "svelte-navigator";
  import { demolist } from "./lib/PackingList/demolist";
  import PackingList from "./lib/PackingList/PackingList.svelte";
  import Navbar from "./lib/ui/Navbar.svelte";
  import UIPreview from "./lib/ui/Preview.svelte";
  import ThemeProvider from "./ThemeProvider.svelte";
</script>

<ThemeProvider>
  <Router>
    <Navbar />

    <main>
      <Route path="/">
        <PackingList packingList={demolist} />
      </Route>

      <Route path="/components">
        <UIPreview />
      </Route>
    </main>
  </Router>
</ThemeProvider>
