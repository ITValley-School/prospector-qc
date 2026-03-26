<script lang="ts">
	import { page } from '$app/state';

	const links = [
		{ href: '/', label: 'Prospectar' },
		{ href: '/resultados', label: 'Resultados' },
		{ href: '/historico', label: 'Historico' },
		{ href: '/configuracoes', label: 'Configuracoes' },
	];
</script>

<nav class="bg-navy border-b border-border sticky top-0 z-40">
	<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
		<div class="flex items-center justify-between h-16">
			<a href="/" class="flex items-center gap-3">
				<div class="w-8 h-8 bg-gradient-to-br from-accent to-success rounded-lg flex items-center justify-center">
					<span class="text-white font-bold text-sm">PQ</span>
				</div>
				<span class="text-text-heading font-semibold text-lg">Prospector QC</span>
			</a>
			<div class="flex items-center gap-1">
				{#each links as link}
					<a
						href={link.href}
						class="px-3 py-2 rounded-lg text-sm font-medium transition-colors {page.url.pathname === link.href ? 'bg-accent/10 text-accent' : 'text-text-muted hover:text-text hover:bg-card'}"
					>
						{link.label}
					</a>
				{/each}
			</div>
		</div>
	</div>
</nav>
