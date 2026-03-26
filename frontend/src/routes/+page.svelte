<script lang="ts">
	import { goto } from '$app/navigation';
	import Card from '$lib/components/ui/Card.svelte';
	import Button from '$lib/components/ui/Button.svelte';
	import Input from '$lib/components/ui/Input.svelte';
	import Select from '$lib/components/ui/Select.svelte';
	import ProgressBar from '$lib/components/ui/ProgressBar.svelte';
	import { ProspectionRequest } from '$lib/dtos/prospection';
	import { ProspectionService } from '$lib/services/prospection-service';
	import { WebSocketService } from '$lib/services/websocket-service';

	let titulo = $state('');
	let segmento = $state('');
	let localizacao = $state('');
	let quantidade_leads = $state(10);
	let prompt_customizado = $state('');
	let loading = $state(false);
	let progresso = $state(0);
	let statusMsg = $state('');
	let erro = $state('');

	const engineOptions = [
		{ value: 'claude_code', label: 'Claude Code CLI' },
		{ value: 'ai_api', label: 'IA API (OpenAI/Anthropic/Google)' },
	];
	let engine_tipo = $state('claude_code');

	const wsService = new WebSocketService();

	function handleProspeccaoClick(node: HTMLElement) {
		const handler = () => iniciarProspeccao();
		node.addEventListener('click', handler);
		return { destroy() { node.removeEventListener('click', handler); } };
	}

	async function iniciarProspeccao() {
		const dto = new ProspectionRequest({
			titulo, segmento, localizacao, quantidade_leads, prompt_customizado, engine_tipo,
		});

		if (!dto.isValid()) {
			erro = 'Preencha titulo e segmento';
			return;
		}

		loading = true;
		erro = '';
		progresso = 5;
		statusMsg = 'Iniciando prospeccao...';

		try {
			const result = await ProspectionService.criar(dto.toPayload());

			wsService.connect(result.id, (data: any) => {
				if (data.progresso) progresso = data.progresso;
				if (data.status === 'processando') statusMsg = 'IA analisando mercado...';
				if (data.status === 'parseando') statusMsg = 'Organizando leads...';
				if (data.status === 'concluido') {
					statusMsg = `Concluido! ${data.total_leads} leads encontrados`;
					loading = false;
					wsService.disconnect();
					setTimeout(() => goto(`/resultados/${result.id}`), 1500);
				}
				if (data.status === 'erro') {
					erro = data.erro || 'Erro desconhecido';
					loading = false;
					wsService.disconnect();
				}
			});
		} catch (e: any) {
			erro = e.message || 'Erro ao iniciar prospeccao';
			loading = false;
		}
	}
</script>

<div class="space-y-8">
	<div>
		<h1 class="text-3xl font-bold text-text-heading">Nova Prospeccao</h1>
		<p class="text-text-muted mt-2">Encontre leads qualificados usando IA multi-motor</p>
	</div>

	<Card>
		<div class="space-y-6">
			<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
				<Input label="Titulo da prospeccao" placeholder="Ex: Empresas de tecnologia em SP" bind:value={titulo} />
				<Input label="Segmento" placeholder="Ex: Tecnologia da Informacao" bind:value={segmento} />
			</div>

			<div class="grid grid-cols-1 md:grid-cols-3 gap-6">
				<Input label="Localizacao" placeholder="Ex: Sao Paulo, SP" bind:value={localizacao} />
				<Input label="Quantidade de leads" type="number" bind:value={quantidade_leads} />
				<Select label="Engine de IA" options={engineOptions} bind:value={engine_tipo} />
			</div>

			<div>
				<label class="block text-sm font-medium text-text-muted mb-1.5">Instrucoes adicionais (opcional)</label>
				<textarea
					bind:value={prompt_customizado}
					placeholder="Ex: Priorize empresas com mais de 100 funcionarios..."
					rows="3"
					class="w-full bg-navy border border-border rounded-lg px-4 py-2.5 text-text placeholder-text-muted/50 focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent/30 transition-colors resize-none"
				></textarea>
			</div>

			{#if erro}
				<div class="bg-danger/10 border border-danger/30 rounded-lg p-4 text-danger text-sm">{erro}</div>
			{/if}

			{#if loading}
				<div class="space-y-3">
					<ProgressBar value={progresso} label={statusMsg} />
				</div>
			{/if}

			<div class="flex gap-3">
				<button
					use:handleProspeccaoClick
					class="inline-flex items-center justify-center font-medium rounded-lg transition-all duration-200 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed bg-accent hover:bg-accent-hover text-white shadow-lg shadow-accent/20 px-6 py-3 text-base gap-2.5"
					disabled={loading}
				>
					{#if loading}
						<svg class="animate-spin h-4 w-4" viewBox="0 0 24 24">
							<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"></circle>
							<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
						</svg>
					{/if}
					Prospectar com {engine_tipo === 'claude_code' ? 'Claude Code' : 'IA API'}
				</button>
			</div>
		</div>
	</Card>
</div>
