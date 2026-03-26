const WS_BASE = import.meta.env.VITE_WS_URL || 'ws://localhost:8002';

export class WebSocketService {
	private ws: WebSocket | null = null;

	connect(prospectionId: string, onMessage: (data: any) => void) {
		this.ws = new WebSocket(`${WS_BASE}/ws/prospection/${prospectionId}`);

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
	}
}
