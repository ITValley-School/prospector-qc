<script lang="ts">
	import type { Snippet } from 'svelte';

	interface Props {
		hover?: boolean;
		children: Snippet;
	}

	let { hover = false, children }: Props = $props();
</script>

<div class="bg-card border border-border rounded-xl p-6 {hover ? 'hover:bg-card-hover hover:border-accent/30 transition-all duration-200 cursor-pointer' : ''}">
	{@render children()}
</div>
