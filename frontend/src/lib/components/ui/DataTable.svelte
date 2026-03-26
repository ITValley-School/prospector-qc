<script lang="ts">
	interface Column {
		key: string;
		label: string;
		width?: string;
	}

	interface Props {
		columns: Column[];
		data: Record<string, any>[];
		onrowclick?: (row: Record<string, any>) => void;
	}

	let { columns, data, onrowclick }: Props = $props();
</script>

<div class="overflow-x-auto rounded-xl border border-border">
	<table class="w-full">
		<thead>
			<tr class="bg-navy/50">
				{#each columns as col}
					<th class="px-4 py-3 text-left text-xs font-semibold text-text-muted uppercase tracking-wider" style={col.width ? `width: ${col.width}` : ''}>
						{col.label}
					</th>
				{/each}
			</tr>
		</thead>
		<tbody>
			{#each data as row, i}
				<tr
					class="border-t border-border/50 hover:bg-card-hover transition-colors {onrowclick ? 'cursor-pointer' : ''}"
					onclick={() => onrowclick?.(row)}
				>
					{#each columns as col}
						<td class="px-4 py-3 text-sm text-text">
							{row[col.key] ?? '-'}
						</td>
					{/each}
				</tr>
			{/each}
			{#if data.length === 0}
				<tr>
					<td colspan={columns.length} class="px-4 py-8 text-center text-text-muted text-sm">
						Nenhum dado encontrado
					</td>
				</tr>
			{/if}
		</tbody>
	</table>
</div>
