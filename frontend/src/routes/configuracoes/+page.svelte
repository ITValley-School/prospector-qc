<script lang="ts">
	import Card from '$lib/components/ui/Card.svelte';
	import Button from '$lib/components/ui/Button.svelte';
	import Input from '$lib/components/ui/Input.svelte';
	import Select from '$lib/components/ui/Select.svelte';
	import Badge from '$lib/components/ui/Badge.svelte';
	import { EngineService } from '$lib/services/engine-service';
	import { EngineConfigRequest } from '$lib/dtos/engine';
	import type { EngineConfig } from '$lib/dtos/engine';

	let engines = $state<EngineConfig[]>([]);
	let loading = $state(true);
	let saving = $state(false);
	let message = $state('');
	let pipelineAberto = $state(false);

	let engine_tipo = $state('ai_api');
	let provider = $state('openai');
	let modelo = $state('gpt-4o');
	let api_key_ref = $state('');

	const providerOptions = [
		{ value: 'openai', label: 'OpenAI' },
		{ value: 'anthropic', label: 'Anthropic' },
		{ value: 'google', label: 'Google (Gemini)' },
	];

	const modelosPorProvider: Record<string, { value: string; label: string }[]> = {
		openai: [
			{ value: 'gpt-4o', label: 'GPT-4o' },
			{ value: 'gpt-4o-mini', label: 'GPT-4o Mini' },
		],
		anthropic: [
			{ value: 'claude-sonnet-4-20250514', label: 'Claude Sonnet 4' },
			{ value: 'claude-haiku-4-5-20251001', label: 'Claude Haiku 4.5' },
		],
		google: [
			{ value: 'gemini-2.0-flash', label: 'Gemini 2.0 Flash' },
			{ value: 'gemini-2.5-pro-preview-05-06', label: 'Gemini 2.5 Pro' },
		],
	};

	let modeloOptions = $derived(modelosPorProvider[provider] || []);

	$effect(() => {
		loadData();
	});

	async function loadData() {
		try {
			engines = await EngineService.listar();
		} catch (e) {
			console.error(e);
		} finally {
			loading = false;
		}
	}

	async function salvar() {
		const dto = new EngineConfigRequest({ engine_tipo, provider, modelo, api_key_ref });
		if (!dto.isValid()) return;

		saving = true;
		message = '';
		try {
			await EngineService.configurar(dto.toPayload());
			message = 'Configuracao salva com sucesso!';
			await loadData();
		} catch (e: any) {
			message = 'Erro: ' + (e.message || 'Falha ao salvar');
		} finally {
			saving = false;
		}
	}
</script>

<div class="space-y-8">
	<div>
		<h1 class="text-3xl font-bold text-text-heading">Configuracoes</h1>
		<p class="text-text-muted mt-2">Configure as engines de IA e chaves de API</p>
	</div>

	<Card>
		<h2 class="text-xl font-semibold text-text-heading mb-6">Configurar Engine IA API</h2>
		<div class="space-y-4">
			<div class="grid grid-cols-1 md:grid-cols-3 gap-4">
				<Select label="Provider" options={providerOptions} bind:value={provider} />
				<Select label="Modelo" options={modeloOptions} bind:value={modelo} />
				<Input label="API Key (referencia)" placeholder="Nome da env var" bind:value={api_key_ref} />
			</div>

			{#if message}
				<div class="text-sm {message.startsWith('Erro') ? 'text-danger' : 'text-success'}">{message}</div>
			{/if}

			<Button onclick={salvar} loading={saving}>Salvar configuracao</Button>
		</div>
	</Card>

	<Card>
		<h2 class="text-xl font-semibold text-text-heading mb-4">Engines configuradas</h2>
		{#if loading}
			<div class="text-text-muted">Carregando...</div>
		{:else if engines.length === 0}
			<div class="text-text-muted">Nenhuma engine configurada</div>
		{:else}
			<div class="space-y-3">
				{#each engines as eng}
					<div class="flex items-center justify-between p-4 bg-navy rounded-lg border border-border">
						<div>
							<span class="font-medium text-text-heading">{eng.engine_tipo}</span>
							{#if eng.provider}
								<span class="text-text-muted ml-2">({eng.provider} / {eng.modelo})</span>
							{/if}
						</div>
						<Badge text={eng.ativo ? 'Ativo' : 'Inativo'} variant={eng.ativo ? 'success' : 'default'} />
					</div>
				{/each}
			</div>
		{/if}
	</Card>

	<Card>
		<button
			class="w-full flex items-center justify-between text-left"
			onclick={() => pipelineAberto = !pipelineAberto}
		>
			<h2 class="text-xl font-semibold text-text-heading">Pipeline de Busca</h2>
			<span class="text-accent text-2xl transition-transform {pipelineAberto ? 'rotate-180' : ''}"
				>&#9660;</span
			>
		</button>

		{#if pipelineAberto}
			<div class="mt-6 space-y-4 text-sm">
				<p class="text-text-muted">
					Fluxo completo desde o clique em "Prospectar" ate os leads aparecerem na tela e serem salvos no datalake.
				</p>

				<div class="space-y-3">
					<!-- Etapa 1 -->
					<div class="p-4 bg-navy rounded-lg border border-border">
						<div class="flex items-center gap-3 mb-2">
							<span class="bg-accent text-navy font-bold rounded-full w-7 h-7 flex items-center justify-center text-xs">1</span>
							<span class="font-semibold text-text-heading">Validacao</span>
						</div>
						<p class="text-text-muted ml-10">Titulo, segmento, engine (claude_code | ai_api), quantidade (1-50). Salva no SQL Server com status "pendente".</p>
						<code class="text-xs text-accent ml-10">factories/prospection_factory.py → criar_prospection()</code>
					</div>

					<!-- Etapa 2 -->
					<div class="p-4 bg-navy rounded-lg border border-border">
						<div class="flex items-center gap-3 mb-2">
							<span class="bg-accent text-navy font-bold rounded-full w-7 h-7 flex items-center justify-center text-xs">2</span>
							<span class="font-semibold text-text-heading">Montagem do Prompt</span>
						</div>
						<p class="text-text-muted ml-10">Injeta segmento, localizacao, quantidade e instrucoes customizadas no template de prompt B2B.</p>
						<code class="text-xs text-accent ml-10">factories/prospection_factory.py → montar_prompt_prospeccao()</code>
					</div>

					<!-- Etapa 3 -->
					<div class="p-4 bg-navy rounded-lg border border-border">
						<div class="flex items-center gap-3 mb-2">
							<span class="bg-accent text-navy font-bold rounded-full w-7 h-7 flex items-center justify-center text-xs">3</span>
							<span class="font-semibold text-text-heading">Execucao da Engine</span>
						</div>
						<p class="text-text-muted ml-10">
							<strong>Claude Code CLI:</strong> <code class="bg-dark px-1 rounded">claude -p "prompt" --output-format json</code><br />
							<strong>AI API:</strong> OpenAI (gpt-4o) | Anthropic (claude-sonnet) | Google (gemini-2.0-flash)
						</p>
						<code class="text-xs text-accent ml-10">engines/claude_code_engine.py | engines/ai_api_engine.py</code>
					</div>

					<!-- Etapa 4 -->
					<div class="p-4 bg-navy rounded-lg border border-border">
						<div class="flex items-center gap-3 mb-2">
							<span class="bg-accent text-navy font-bold rounded-full w-7 h-7 flex items-center justify-center text-xs">4</span>
							<span class="font-semibold text-text-heading">Parsing do Resultado</span>
						</div>
						<p class="text-text-muted ml-10">Remove markdown, encontra JSON array no texto, valida estrutura. Cada item vira um Lead + Contatos.</p>
						<code class="text-xs text-accent ml-10">factories/lead_factory.py → parsear_resultado_ia()</code>
					</div>

					<!-- Etapa 5 -->
					<div class="p-4 bg-navy rounded-lg border border-border">
						<div class="flex items-center gap-3 mb-2">
							<span class="bg-accent text-navy font-bold rounded-full w-7 h-7 flex items-center justify-center text-xs">5</span>
							<span class="font-semibold text-text-heading">Criacao de Leads</span>
						</div>
						<p class="text-text-muted ml-10">Para cada item do array: cria Lead no banco (nome, segmento, website, descricao, score) + LeadContacts (nome, cargo, email, telefone, linkedin).</p>
						<code class="text-xs text-accent ml-10">factories/lead_factory.py → criar_lead_from_dict() + criar_contatos_from_dict()</code>
					</div>

					<!-- Etapa 6 -->
					<div class="p-4 bg-navy rounded-lg border border-border">
						<div class="flex items-center gap-3 mb-2">
							<span class="bg-accent text-navy font-bold rounded-full w-7 h-7 flex items-center justify-center text-xs">6</span>
							<span class="font-semibold text-text-heading">Auto-Export Datalake</span>
						</div>
						<p class="text-text-muted ml-10">Gera JSON com leads + contatos, faz upload no Azure Blob Storage (saprospectorqc/sistemaprospect). URL salva na prospection.</p>
						<code class="text-xs text-accent ml-10">services/export_service.py → exportar_leads() | data/connections/blob_storage.py</code>
					</div>
				</div>

				<div class="p-4 bg-dark rounded-lg border border-border mt-4">
					<p class="text-text-muted text-xs">
						Documentacao completa: <code class="text-accent">.claude/skills/pipelinesearch.md</code>
					</p>
				</div>
			</div>
		{/if}
	</Card>

	<Card>
		<h2 class="text-xl font-semibold text-text-heading mb-4">Claude Code CLI</h2>
		<p class="text-text-muted text-sm">
			O engine Claude Code CLI usa o binario <code class="bg-navy px-2 py-0.5 rounded text-accent">claude</code> instalado localmente.
			Nao requer configuracao adicional de API key — usa a autenticacao do CLI.
		</p>
		<div class="mt-3">
			<Badge text="Sempre disponivel" variant="success" />
		</div>
	</Card>
</div>
