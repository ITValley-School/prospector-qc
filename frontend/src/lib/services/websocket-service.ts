function getWsBase() {
	if (import.meta.env.VITE_WS_URL) return import.meta.env.VITE_WS_URL;
	if (typeof window !== 'undefined') {
		const proto = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
		return `${proto}//${window.location.host}`;
	}
	return 'ws://localhost:8002';
}
const USE_MOCK = import.meta.env.VITE_USE_MOCK === 'true';

export class WebSocketService {
	private ws: WebSocket | null = null;
	private mockTimer: ReturnType<typeof setTimeout> | null = null;

	connect(prospectionId: string, onMessage: (data: any) => void) {
		if (USE_MOCK) {
			this.simulateMock(onMessage);
			return;
		}

		const wsBase = getWsBase();
		this.ws = new WebSocket(`${wsBase}/ws/prospection/${prospectionId}`);

		this.ws.onmessage = (event) => {
			const data = JSON.parse(event.data);
			onMessage(data);
		};

		this.ws.onerror = () => {
			console.error('WebSocket error');
		};

		this.ws.onclose = () => {
			this.ws = null;
		};
	}

	disconnect() {
		this.ws?.close();
		this.ws = null;
		if (this.mockTimer) {
			clearTimeout(this.mockTimer);
			this.mockTimer = null;
		}
	}

	private simulateMock(onMessage: (data: any) => void) {
		const steps = [
			{ delay: 500, data: { progresso: 20, status: 'processando' } },
			{ delay: 1500, data: { progresso: 50, status: 'processando' } },
			{ delay: 2500, data: { progresso: 75, status: 'parseando' } },
			{ delay: 3500, data: { progresso: 100, status: 'concluido', total_leads: 5 } },
		];

		for (const step of steps) {
			this.mockTimer = setTimeout(() => onMessage(step.data), step.delay);
		}
	}
}
