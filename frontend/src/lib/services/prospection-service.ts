import { criarProspection, listarProspections, buscarProspection, exportarLeads } from '$lib/repositories/prospection-repository';

export class ProspectionService {
	static async criar(payload: Record<string, any>) {
		return criarProspection(payload);
	}

	static async listar() {
		return listarProspections();
	}

	static async buscar(id: string) {
		return buscarProspection(id);
	}

	static async exportar(id: string, formato: string = 'csv') {
		return exportarLeads(id, formato);
	}
}
