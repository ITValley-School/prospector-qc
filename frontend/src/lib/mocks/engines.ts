import type { EngineConfig } from '$lib/dtos/engine';

export const mockEngines: EngineConfig[] = [
	{ id: 'eng-1', engine_tipo: 'claude_code', provider: null, modelo: null, ativo: true },
	{ id: 'eng-2', engine_tipo: 'ai_api', provider: 'openai', modelo: 'gpt-4o', ativo: true },
	{ id: 'eng-3', engine_tipo: 'ai_api', provider: 'google', modelo: 'gemini-2.0-flash', ativo: false },
];
