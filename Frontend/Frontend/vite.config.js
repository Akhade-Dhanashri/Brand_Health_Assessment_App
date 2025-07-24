import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

<<<<<<< HEAD
export default defineConfig({
  plugins: [react()],
})
=======
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
>>>>>>> 603d2109acaa10edc3700f9a45fa447af1b9b05f
