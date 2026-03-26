<script>
	import '../app.css';
	import Navbar from '$lib/components/layout/Navbar.svelte';

	let { children } = $props();
</script>

<svelte:head>
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
	<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet" />
	<title>Prospector QC</title>
</svelte:head>

<div class="min-h-screen bg-page">
	<Navbar />
	<main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
		{@render children()}
	</main>
</div>
