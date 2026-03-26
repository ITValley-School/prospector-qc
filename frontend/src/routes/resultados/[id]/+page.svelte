<script lang="ts">
	import { page } from '$app/state';
	import Card from '$lib/components/ui/Card.svelte';
	import Badge from '$lib/components/ui/Badge.svelte';
	import Button from '$lib/components/ui/Button.svelte';
	import DataTable from '$lib/components/ui/DataTable.svelte';
	import { ProspectionService } from '$lib/services/prospection-service';
	import { getStatusBadgeVariant, getStatusLabel, formatDate } from '$lib/utils/status';
	import type { ProspectionDetalhe } from '$lib/dtos/prospection';

	let prospection = $state<ProspectionDetalhe | null>(null);
	let loading = $state(true);
	let exporting = $state(false);

	const columns = [
		{ key: 'nome_empresa', label: 'Empresa' },
		{ key: 'segmento', label: 'Segmento' },
		{ key: 'website', label: 'Website' },
		{ key: 'score', label: 'Score', width: '80px' },
		{ key: 'status', label: 'Status', width: '100px' },
	];

	$effect(() => {
		loadData();
	});

	async function loadData() {
		try {
			prospection = await ProspectionService.buscar(page.params.id);
		} catch (e) {
			console.error(e);
		} finally {
			loading = false;
		}
	}

	async function exportar(formato: string) {
		if (!prospection) return;
		exporting = true;
		try {
			const result = await ProspectionService.exportar(prospection.id, formato);
			if (result.url && result.url !== '#') {
				window.open(result.url, '_blank');
			}
		} catch (e) {
			console.error(e);
		} finally {
			exporting = false;
		}
	}
</script>

<div class="space-y-8">
	{#if loading}
		<div class="text-center py-12 text-text-muted">Carregando...</div>
	{:else if prospection}
		<div class="flex items-start justify-between">
			<div>
				<div class="flex items-center gap-3">
					<h1 class="text-3xl font-bold text-text-heading">{prospection.titulo}</h1>
					<Badge text={getStatusLabel(prospection.status)} variant={getStatusBadgeVariant(prospection.status)} />
				</div>
				<p class="text-text-muted mt-2">
					{prospection.segmento} {prospection.localizacao ? `- ${prospection.localizacao}` : ''}
				</p>
			</div>
			<div class="flex gap-2">
				<Button variant="secondary" size="sm" onclick={() => exportar('csv')} loading={exporting}>
					Exportar CSV
				</Button>
				<Button variant="secondary" size="sm" onclick={() => exportar('json')} loading={exporting}>
					Exportar JSON
				</Button>
			</div>
		</div>

		<div class="grid grid-cols-1 md:grid-cols-4 gap-4">
			<Card>
				<div class="text-center">
					<div class="text-3xl font-bold text-accent">{prospection.total_leads_encontrados}</div>
					<div class="text-sm text-text-muted mt-1">Leads encontrados</div>
				</div>
			</Card>
			<Card>
				<div class="text-center">
					<div class="text-3xl font-bold text-text-heading">{prospection.quantidade_leads}</div>
					<div class="text-sm text-text-muted mt-1">Leads solicitados</div>
				</div>
			</Card>
			<Card>
				<div class="text-center">
					<div class="text-lg font-semibold text-text-heading">{prospection.engine_tipo === 'claude_code' ? 'Claude Code' : 'IA API'}</div>
					<div class="text-sm text-text-muted mt-1">Engine utilizada</div>
				</div>
			</Card>
			<Card>
				<div class="text-center">
					<div class="text-lg font-semibold text-text-heading">{formatDate(prospection.criado_em)}</div>
					<div class="text-sm text-text-muted mt-1">Data da prospeccao</div>
				</div>
			</Card>
		</div>

		{#if prospection.erro}
			<div class="bg-danger/10 border border-danger/30 rounded-lg p-4 text-danger text-sm">
				{prospection.erro}
			</div>
		{/if}

		<div>
			<h2 class="text-xl font-semibold text-text-heading mb-4">Leads encontrados</h2>
			<DataTable
				{columns}
				data={prospection.leads.map(l => ({ ...l, score: l.score.toFixed(1) }))}
			/>
		</div>

		{#if prospection.arquivo_export_url}
			<Card>
				<div class="flex items-center justify-between">
					<span class="text-text-muted">Arquivo exportado:</span>
					<a href={prospection.arquivo_export_url} target="_blank" class="text-accent hover:underline">
						Download
					</a>
				</div>
			</Card>
		{/if}
	{:else}
		<div class="text-center py-12 text-text-muted">Prospeccao nao encontrada</div>
	{/if}
</div>
