export interface LeadDetalhe {
	id: string;
	prospection_id: string;
	nome_empresa: string;
	segmento: string | null;
	website: string | null;
	descricao: string | null;
	score: number;
	status: string;
	contatos: Contato[];
	criado_em: string;
}

export interface Contato {
	id: string;
	nome: string | null;
	cargo: string | null;
	email: string | null;
	telefone: string | null;
	linkedin: string | null;
}
