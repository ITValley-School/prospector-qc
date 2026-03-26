<script lang="ts">
	import { goto } from '$app/navigation';
	import Card from '$lib/components/ui/Card.svelte';
	import Badge from '$lib/components/ui/Badge.svelte';
	import DataTable from '$lib/components/ui/DataTable.svelte';
	import { ProspectionService } from '$lib/services/prospection-service';
	import { getStatusBadgeVariant, getStatusLabel, formatDate } from '$lib/utils/status';
	import type { ProspectionResumo } from '$lib/dtos/prospection';

	let prospections = $state<ProspectionResumo[]>([]);
	let loading = $state(true);

	$effect(() => {
		loadData();
	});

	async function loadData() {
		try {
			prospections = await ProspectionService.listar();
		} catch (e) {
			console.error(e);
		} finally {
			loading = false;
		}
	}
</script>

<div class="space-y-8">
	<div>
		<h1 class="text-3xl font-bold text-text-heading">Resultados</h1>
		<p class="text-text-muted mt-2">Todas as prospeccoes realizadas</p>
	</div>

	{#if loading}
		<div class="text-center py-12 text-text-muted">Carregando...</div>
	{:else if prospections.length === 0}
		<Card>
			<div class="text-center py-8">
				<p class="text-text-muted">Nenhuma prospeccao realizada ainda.</p>
				<a href="/" class="text-accent hover:underline mt-2 inline-block">Criar primeira prospeccao</a>
			</div>
		</Card>
	{:else}
		<div class="grid gap-4">
			{#each prospections as p}
				<Card hover>
					<a href="/resultados/{p.id}" class="block">
						<div class="flex items-center justify-between">
							<div>
								<h3 class="text-lg font-semibold text-text-heading">{p.titulo}</h3>
								<p class="text-text-muted text-sm mt-1">{p.segmento} {p.localizacao ? `- ${p.localizacao}` : ''}</p>
							</div>
							<div class="flex items-center gap-4">
								<div class="text-right">
									<div class="text-2xl font-bold text-accent">{p.total_leads_encontrados}</div>
									<div class="text-xs text-text-muted">leads</div>
								</div>
								<Badge text={getStatusLabel(p.status)} variant={getStatusBadgeVariant(p.status)} />
							</div>
						</div>
						<div class="flex items-center gap-4 mt-3 text-xs text-text-muted">
							<span>{p.engine_tipo === 'claude_code' ? 'Claude Code' : 'IA API'}</span>
							<span>{formatDate(p.criado_em)}</span>
						</div>
					</a>
				</Card>
			{/each}
		</div>
	{/if}
</div>
