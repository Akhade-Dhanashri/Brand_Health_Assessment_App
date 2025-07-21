import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

/*export default defineConfig({
  plugins: [react()],
})*/
export default {
  server: {
    host: '0.0.0.0',  // Allows external access
    port: 5173,
    strictPort: true   // Prevents automatic port switching
  }
}