/**
 * main.ts
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Plugins
import { registerPlugins } from '@/plugins'
import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";
// Components
import App from './App.vue'

// Composables
import { createApp } from 'vue'
import { createPinia } from 'pinia'


const app = createApp(App)
registerPlugins(app)
app.use(Toast, {
  // Add any custom options here if desired, e.g., timeout, position, etc.
});
// Suppress Vue warnings
app.config.warnHandler = function (msg, vm, trace) {
  // Suppress all warnings
  return;
};

// Alternatively, to suppress all logs including warnings
// app.config.silent = true;

const pinia = createPinia()
app.use(pinia)

app.mount('#app')
