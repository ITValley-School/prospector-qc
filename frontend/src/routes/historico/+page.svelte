<script lang="ts">
	import Card from '$lib/components/ui/Card.svelte';
	import Input from '$lib/components/ui/Input.svelte';
	import Badge from '$lib/components/ui/Badge.svelte';
	import { ProspectionService } from '$lib/services/prospection-service';
	import { getStatusBadgeVariant, getStatusLabel, formatDate } from '$lib/utils/status';
	import type { ProspectionResumo } from '$lib/dtos/prospection';

	let prospections = $state<ProspectionResumo[]>([]);
	let loading = $state(true);
	let filtro = $state('');

	let filtradas = $derived(
		prospections.filter(p =>
			p.titulo.toLowerCase().includes(filtro.toLowerCase()) ||
			p.segmento.toLowerCase().includes(filtro.toLowerCase())
		)
	);

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
	<div class="flex items-start justify-between">
		<div>
			<h1 class="text-3xl font-bold text-text-heading">Historico</h1>
			<p class="text-text-muted mt-2">Todas as prospeccoes realizadas</p>
		</div>
		<div class="w-72">
			<Input placeholder="Buscar por titulo ou segmento..." bind:value={filtro} />
		</div>
	</div>

	{#if loading}
		<div class="text-center py-12 text-text-muted">Carregando...</div>
	{:else if filtradas.length === 0}
		<Card>
			<div class="text-center py-8 text-text-muted">Nenhuma prospeccao encontrada</div>
		</Card>
	{:else}
		<div class="space-y-3">
			{#each filtradas as p}
				<a href="/resultados/{p.id}" class="block">
					<Card hover>
						<div class="flex items-center justify-between">
							<div class="flex items-center gap-4">
								<div>
									<h3 class="font-semibold text-text-heading">{p.titulo}</h3>
									<p class="text-sm text-text-muted">{p.segmento} {p.localizacao ? `- ${p.localizacao}` : ''}</p>
								</div>
							</div>
							<div class="flex items-center gap-6">
								<span class="text-sm text-text-muted">{formatDate(p.criado_em)}</span>
								<span class="text-sm font-medium text-accent">{p.total_leads_encontrados} leads</span>
								<Badge text={getStatusLabel(p.status)} variant={getStatusBadgeVariant(p.status)} />
							</div>
						</div>
					</Card>
				</a>
			{/each}
		</div>
	{/if}
</div>
