export interface EngineConfig {
	id: string;
	engine_tipo: string;
	provider: string | null;
	modelo: string | null;
	ativo: boolean;
}

export class EngineConfigRequest {
	readonly engine_tipo: string;
	readonly provider: string;
	readonly modelo: string;
	readonly api_key_ref: string;

	constructor(data: Record<string, any>) {
		this.engine_tipo = data.engine_tipo ?? '';
		this.provider = data.provider ?? '';
		this.modelo = data.modelo ?? '';
		this.api_key_ref = data.api_key_ref ?? '';
	}

	isValid(): boolean {
		return this.engine_tipo.trim().length > 0;
	}

	toPayload(): Record<string, any> {
		return {
			engine_tipo: this.engine_tipo,
			provider: this.provider || null,
			modelo: this.modelo || null,
			api_key_ref: this.api_key_ref || null,
		};
	}
}
