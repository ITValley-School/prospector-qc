export function getStatusBadgeVariant(status: string): 'default' | 'success' | 'warning' | 'danger' | 'info' {
	switch (status) {
		case 'concluido': return 'success';
		case 'processando': return 'info';
		case 'pendente': return 'warning';
		case 'erro': return 'danger';
		case 'exportado': return 'success';
		default: return 'default';
	}
}

export function getStatusLabel(status: string): string {
	switch (status) {
		case 'concluido': return 'Concluido';
		case 'processando': return 'Processando';
		case 'pendente': return 'Pendente';
		case 'erro': return 'Erro';
		case 'exportado': return 'Exportado';
		default: return status;
	}
}

export function formatDate(dateStr: string): string {
	return new Date(dateStr).toLocaleDateString('pt-BR', {
		day: '2-digit',
		month: '2-digit',
		year: 'numeric',
		hour: '2-digit',
		minute: '2-digit',
	});
}
