import type { ProspectionResumo, ProspectionDetalhe } from '$lib/dtos/prospection';
import { mockProspections, mockProspectionDetalhe } from '$lib/mocks/prospections';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8002';
const USE_MOCK = import.meta.env.VITE_USE_MOCK === 'true';

export async function criarProspection(payload: Record<string, any>): Promise<any> {
	if (USE_MOCK) {
		const id = Math.random().toString(36).slice(2) + Date.now().toString(36);
		return { ...mockProspectionDetalhe, ...payload, id, status: 'pendente' };
	}
	const res = await fetch(`${API_BASE}/api/prospections`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(payload),
	});
	if (!res.ok) throw new Error(await res.text());
	return res.json();
}

export async function listarProspections(): Promise<ProspectionResumo[]> {
	if (USE_MOCK) return mockProspections;
	const res = await fetch(`${API_BASE}/api/prospections`);
	if (!res.ok) throw new Error(await res.text());
	return res.json();
}

export async function buscarProspection(id: string): Promise<ProspectionDetalhe> {
	if (USE_MOCK) return { ...mockProspectionDetalhe, id };
	const res = await fetch(`${API_BASE}/api/prospections/${id}`);
	if (!res.ok) throw new Error(await res.text());
	return res.json();
}

export async function exportarLeads(id: string, formato: string = 'csv'): Promise<any> {
	if (USE_MOCK) return { url: '#', formato, total_leads: 5 };
	const res = await fetch(`${API_BASE}/api/export/${id}?formato=${formato}`, { method: 'POST' });
	if (!res.ok) throw new Error(await res.text());
	return res.json();
}
