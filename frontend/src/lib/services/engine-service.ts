import { listarEngines, configurarEngine } from '$lib/repositories/engine-repository';

export class EngineService {
	static async listar() {
		return listarEngines();
	}

	static async configurar(payload: Record<string, any>) {
		return configurarEngine(payload);
	}
}
