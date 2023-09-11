<slot />

<style>
  :global(:root) {
    font-family: Inter, Avenir, Helvetica, Arial, sans-serif;
    font-size: 16px;
    line-height: 24px;
    font-weight: 400;
    color-scheme: light dark;

    -moz-text-size-adjust: none;
    -webkit-text-size-adjust: none;
    text-size-adjust: none;

    --light: #f3f2ee;
    --nadeshiko-pink: #edadc7;
    --yuru-blue: #75cdd8;
    --shimarin-blue: #4a4e7d;
    --dark: #313738;

    --light-accent: var(--nadeshiko-pink);
    --dark-accent: var(--shimarin-blue);

    --primary: var(--yuru-blue);
    --secondary: var(--nadeshiko-pink);
    --success: #58b879;
    --warning: #d6a841;
    --danger: #f44336;
  }

  :global(body) {
    background-color: white;
  }
</style>
