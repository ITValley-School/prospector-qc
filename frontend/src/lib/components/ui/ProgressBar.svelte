<script lang="ts">
	interface Props {
		value: number;
		label?: string;
	}

	let { value, label }: Props = $props();
</script>

<div class="space-y-1.5">
	{#if label}
		<div class="flex justify-between text-sm">
			<span class="text-text-muted">{label}</span>
			<span class="text-accent font-medium">{Math.round(value)}%</span>
		</div>
	{/if}
	<div class="w-full h-2 bg-navy rounded-full overflow-hidden">
		<div
			class="h-full bg-gradient-to-r from-accent to-success rounded-full transition-all duration-500"
			style="width: {value}%"
		></div>
	</div>
</div>
