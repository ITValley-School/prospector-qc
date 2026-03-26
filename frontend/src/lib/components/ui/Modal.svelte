<script lang="ts">
	import type { Snippet } from 'svelte';

	interface Props {
		open: boolean;
		title?: string;
		onclose: () => void;
		children: Snippet;
	}

	let { open = $bindable(false), title = '', onclose, children }: Props = $props();
</script>

{#if open}
	<div class="fixed inset-0 z-50 flex items-center justify-center">
		<div class="absolute inset-0 bg-black/60 backdrop-blur-sm" onclick={onclose}></div>
		<div class="relative bg-card border border-border rounded-2xl p-6 w-full max-w-lg mx-4 shadow-2xl">
			{#if title}
				<div class="flex items-center justify-between mb-4">
					<h3 class="text-lg font-semibold text-text-heading">{title}</h3>
					<button onclick={onclose} class="text-text-muted hover:text-text p-1 rounded-lg hover:bg-navy transition-colors">
						<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
						</svg>
					</button>
				</div>
			{/if}
			{@render children()}
		</div>
	</div>
{/if}
