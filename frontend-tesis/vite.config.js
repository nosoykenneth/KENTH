import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'


// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],

  server: {
    proxy: {
      // Prefijos canonicos: paridad con el gateway de produccion.
      '/api/lms': {
        target: 'http://localhost',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api\/lms/, '')
      },
      '/api/ai': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api\/ai/, '')
      },
      // Aliases retrocompatibles: el plugin local_tesisai y la suite proyecto_curso/api_persistente
      // generan URLs con /moodle_api/ hardcoded (por ejemplo, secure_lista.php devuelve
      // courseimage = '/moodle_api/proyecto_curso/...'). Mantenerlos como alias evita tocar
      // el codigo PHP nativo. En produccion el gateway nginx replica este mapeo.
      '/moodle_api': {
        target: 'http://localhost',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/moodle_api/, '')
      },
      '/rag_api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/rag_api/, '')
      }
    }
  }
})
