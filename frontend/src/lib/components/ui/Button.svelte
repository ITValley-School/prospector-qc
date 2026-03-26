<script lang="ts">
	import type { Snippet } from 'svelte';

	interface Props {
		variant?: 'primary' | 'secondary' | 'danger' | 'ghost';
		size?: 'sm' | 'md' | 'lg';
		disabled?: boolean;
		loading?: boolean;
		onclick?: () => void;
		children: Snippet;
	}

	let { variant = 'primary', size = 'md', disabled = false, loading = false, onclick, children }: Props = $props();

	const baseClasses = 'inline-flex items-center justify-center font-medium rounded-lg transition-all duration-200 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed';

	const variantClasses: Record<string, string> = {
		primary: 'bg-accent hover:bg-accent-hover text-white shadow-lg shadow-accent/20',
		secondary: 'bg-card hover:bg-card-hover text-text border border-border',
		danger: 'bg-danger/10 hover:bg-danger/20 text-danger border border-danger/30',
		ghost: 'hover:bg-card text-text-muted hover:text-text',
	};

	const sizeClasses: Record<string, string> = {
		sm: 'px-3 py-1.5 text-sm gap-1.5',
		md: 'px-4 py-2 text-sm gap-2',
		lg: 'px-6 py-3 text-base gap-2.5',
	};
</script>

<button
	class="{baseClasses} {variantClasses[variant]} {sizeClasses[size]}"
	{disabled}
	{onclick}
>
	{#if loading}
		<svg class="animate-spin h-4 w-4" viewBox="0 0 24 24">
			<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"></circle>
			<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
		</svg>
	{/if}
	{@render children()}
</button>
