import type { EngineConfig } from '$lib/dtos/engine';
import { mockEngines } from '$lib/mocks/engines';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8002';
const USE_MOCK = import.meta.env.VITE_USE_MOCK === 'true';

export async function listarEngines(): Promise<EngineConfig[]> {
	if (USE_MOCK) return mockEngines;
	const res = await fetch(`${API_BASE}/api/engines`);
	if (!res.ok) throw new Error(await res.text());
	return res.json();
}

export async function configurarEngine(payload: Record<string, any>): Promise<any> {
	if (USE_MOCK) return { ...payload, id: Math.random().toString(36).slice(2) + Date.now().toString(36), ativo: true };
	const res = await fetch(`${API_BASE}/api/engines`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(payload),
	});
	if (!res.ok) throw new Error(await res.text());
	return res.json();
}
