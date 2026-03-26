import type { ProspectionResumo, ProspectionDetalhe } from '$lib/dtos/prospection';

export const mockProspections: ProspectionResumo[] = [
	{
		id: '1a2b3c4d-5e6f-7890-abcd-ef1234567890',
		titulo: 'Empresas de tecnologia em SP',
		segmento: 'Tecnologia da Informacao',
		localizacao: 'Sao Paulo, SP',
		engine_tipo: 'claude_code',
		status: 'concluido',
		total_leads_encontrados: 15,
		criado_em: '2026-03-25T14:30:00Z',
	},
	{
		id: '2b3c4d5e-6f78-9012-bcde-f12345678901',
		titulo: 'Industrias alimenticias do Sul',
		segmento: 'Industria Alimenticia',
		localizacao: 'Curitiba, PR',
		engine_tipo: 'ai_api',
		status: 'processando',
		total_leads_encontrados: 0,
		criado_em: '2026-03-26T09:15:00Z',
	},
	{
		id: '3c4d5e6f-7890-1234-cdef-123456789012',
		titulo: 'Construtoras em BH',
		segmento: 'Construcao Civil',
		localizacao: 'Belo Horizonte, MG',
		engine_tipo: 'claude_code',
		status: 'pendente',
		total_leads_encontrados: 0,
		criado_em: '2026-03-26T10:00:00Z',
	},
];

export const mockProspectionDetalhe: ProspectionDetalhe = {
	id: '1a2b3c4d-5e6f-7890-abcd-ef1234567890',
	titulo: 'Empresas de tecnologia em SP',
	segmento: 'Tecnologia da Informacao',
	localizacao: 'Sao Paulo, SP',
	quantidade_leads: 15,
	prompt_customizado: null,
	engine_tipo: 'claude_code',
	status: 'concluido',
	total_leads_encontrados: 15,
	erro: null,
	arquivo_export_url: null,
	leads: [
		{ id: 'lead-1', nome_empresa: 'TechCorp Brasil', segmento: 'SaaS', website: 'https://techcorp.com.br', score: 9.2, status: 'novo' },
		{ id: 'lead-2', nome_empresa: 'DataFlow Solutions', segmento: 'Big Data', website: 'https://dataflow.com.br', score: 8.7, status: 'novo' },
		{ id: 'lead-3', nome_empresa: 'CloudBR Sistemas', segmento: 'Cloud Computing', website: 'https://cloudbr.com.br', score: 8.1, status: 'novo' },
		{ id: 'lead-4', nome_empresa: 'InnovaLab Digital', segmento: 'Desenvolvimento', website: 'https://innovalab.com.br', score: 7.5, status: 'novo' },
		{ id: 'lead-5', nome_empresa: 'SecureTI Consultoria', segmento: 'Seguranca', website: 'https://secureti.com.br', score: 7.0, status: 'novo' },
	],
	criado_em: '2026-03-25T14:30:00Z',
	atualizado_em: '2026-03-25T14:35:00Z',
};
