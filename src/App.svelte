<script async script lang="ts">
  import { onMount } from "svelte";
  import { Router, Route } from "svelte-routing";
  import { demolist } from "./lib/PackingList/demolist";
  import PackingList from "./lib/PackingList/PackingList.svelte";
  import Navbar from "./lib/ui/Navbar.svelte";
  import ThemeProvider from "./ThemeProvider.svelte";
  import Footer from "./lib/ui/Footer.svelte";

  onMount(async () => {
    const body = JSON.stringify({
      name: "Erik",
    });
    const response = await (
      await fetch("/api/trips", { method: "POST", body: body })
    ).text();
    console.log(response);
  });
</script>

<ThemeProvider>
  <Router>
    <Navbar />

    <main>
      <Route path="/">
        <PackingList packingList={demolist} />
      </Route>
    </main>
  </Router>
  <Footer />
</ThemeProvider>
