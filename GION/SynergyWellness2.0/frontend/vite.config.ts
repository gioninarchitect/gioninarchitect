import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
    plugins: [react()],
    define: {
        'process.env': {}
    },
    resolve: {
        alias: {
            '@': '/src'
        }
    },
    server: {
        port: 5173,
        proxy: {
            '/api': {
                target: 'http://localhost:5000',
                changeOrigin: true
            }
        }
    }
});