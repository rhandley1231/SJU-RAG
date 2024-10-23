import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  
  // Add server configuration for API proxy
  server: {
    proxy: {
      // Proxy API requests starting with '/api' to Django backend
      '/api': {
        target: 'http://127.0.0.1:8000', // URL where Django backend is running
        changeOrigin: true,
        secure: false,
      },
    },
  },
})
