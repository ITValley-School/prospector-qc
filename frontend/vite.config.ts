import { sveltekit } from '@sveltejs/kit/vite';
import tailwindcss from '@tailwindcss/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [tailwindcss(), sveltekit()],
	server: {
		port: 5175,
		host: '0.0.0.0',
		proxy: {
			'/api': {
				target: 'http://localhost:8002',
				changeOrigin: true,
			},
			'/ws': {
				target: 'ws://localhost:8002',
				ws: true,
			},
			'/health': {
				target: 'http://localhost:8002',
				changeOrigin: true,
			},
		},
	},
});
