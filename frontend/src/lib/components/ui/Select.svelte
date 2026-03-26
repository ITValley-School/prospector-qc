<script lang="ts">
	interface Option {
		value: string;
		label: string;
	}

	interface Props {
		label?: string;
		options: Option[];
		value?: string;
		onchange?: (e: Event) => void;
	}

	let { label, options, value = $bindable(''), onchange }: Props = $props();
</script>

<div class="space-y-1.5">
	{#if label}
		<label class="block text-sm font-medium text-text-muted">{label}</label>
	{/if}
	<select
		bind:value
		{onchange}
		class="w-full bg-navy border border-border rounded-lg px-4 py-2.5 text-text focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent/30 transition-colors appearance-none cursor-pointer"
	>
		{#each options as opt}
			<option value={opt.value}>{opt.label}</option>
		{/each}
	</select>
</div>
