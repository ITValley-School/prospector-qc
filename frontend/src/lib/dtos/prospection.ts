export class ProspectionRequest {
	readonly titulo: string;
	readonly segmento: string;
	readonly localizacao: string;
	readonly quantidade_leads: number;
	readonly prompt_customizado: string;
	readonly engine_tipo: string;

	constructor(data: Record<string, any>) {
		this.titulo = data.titulo ?? '';
		this.segmento = data.segmento ?? '';
		this.localizacao = data.localizacao ?? '';
		this.quantidade_leads = data.quantidade_leads ?? 10;
		this.prompt_customizado = data.prompt_customizado ?? '';
		this.engine_tipo = data.engine_tipo ?? 'claude_code';
	}

	isValid(): boolean {
		return this.titulo.trim().length > 0 && this.segmento.trim().length > 0;
	}

	toPayload(): Record<string, any> {
		return {
			titulo: this.titulo,
			segmento: this.segmento,
			localizacao: this.localizacao || null,
			quantidade_leads: this.quantidade_leads,
			prompt_customizado: this.prompt_customizado || null,
			engine_tipo: this.engine_tipo,
		};
	}
}

export interface ProspectionResumo {
	id: string;
	titulo: string;
	segmento: string;
	localizacao: string | null;
	engine_tipo: string;
	status: string;
	total_leads_encontrados: number;
	criado_em: string;
}

export interface ProspectionDetalhe {
	id: string;
	titulo: string;
	segmento: string;
	localizacao: string | null;
	quantidade_leads: number;
	prompt_customizado: string | null;
	engine_tipo: string;
	status: string;
	total_leads_encontrados: number;
	erro: string | null;
	arquivo_export_url: string | null;
	leads: LeadResumo[];
	criado_em: string;
	atualizado_em: string;
}

export interface LeadResumo {
	id: string;
	nome_empresa: string;
	segmento: string | null;
	website: string | null;
	score: number;
	status: string;
}
