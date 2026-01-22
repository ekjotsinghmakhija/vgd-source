<script lang="ts">
  import "../app.css";

  let { children } = $props();
</script>

<svelte:head>
  <title>VGD</title>
  <meta name="description" content="VGD - Distributed AI Cluster Dashboard" />
</svelte:head>

<div class="min-h-screen bg-background text-foreground">
  {@render children?.()}
</div>
