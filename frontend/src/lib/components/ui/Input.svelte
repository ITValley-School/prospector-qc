<script lang="ts">
	interface Props {
		label?: string;
		placeholder?: string;
		value?: string;
		type?: string;
		required?: boolean;
		oninput?: (e: Event) => void;
	}

	let { label, placeholder = '', value = $bindable(''), type = 'text', required = false, oninput }: Props = $props();
</script>

<div class="space-y-1.5">
	{#if label}
		<label class="block text-sm font-medium text-text-muted">{label}</label>
	{/if}
	<input
		{type}
		{placeholder}
		{required}
		bind:value
		{oninput}
		class="w-full bg-navy border border-border rounded-lg px-4 py-2.5 text-text placeholder-text-muted/50 focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent/30 transition-colors"
	/>
</div>
