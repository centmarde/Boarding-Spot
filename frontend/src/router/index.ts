/**
 * router/index.ts
 *
 * Automatic routes for `./src/pages/*.vue`
 */

// Composables
import { createRouter, createWebHistory } from 'vue-router/auto'
import { setupLayouts } from 'virtual:generated-layouts'
import { useAuthUserStore } from '../stores/authUser';
import { useToast } from 'vue-toastification';

import Hero from '../pages/index.vue';
import Home from '../pages/Home.vue';
import NotFound from '../pages/NotFound.vue';
import LandLord from '../pages/LandLord.vue';
import Profiles from '../pages/Profiles.vue';

const toast = useToast();

const routes = setupLayouts([
  { path: '/', component: Hero },
  { path: '/home', component: Home, name: 'Home', meta: { requiresAuth: true }, },
  
  { path: '/landlord', component: LandLord, name: 'LandLord', meta: { requiresAuth: true, role: 'landlord' }, },
  { path: '/profiles', component: Profiles, name: 'Profiles', meta: { requiresAuth: true }, },
  { path: '/:pathMatch(.*)*', component: NotFound, name: 'NotFound', },
]);

const router = createRouter({
  history: createWebHistory("/"),
  routes,
});

router.beforeEach((to, from, next) => {
  const isLoggedIn = localStorage.getItem("access_token") !== null;
  console.log(isLoggedIn);
  // Access userRole directly from the store or fallback to localStorage
  const authUserStore = useAuthUserStore();
  const userRole = localStorage.getItem("user_type");
  console.log(userRole);

  // Define public, landlord, and tenant pages
  const publicPages = ["/"];
  const landlordPages = ["/landlord"];
  const tenantPages = ["/home"];

  if (to.meta.requiresAuth && !isLoggedIn) {
    return next("/");
  }

  if (publicPages.includes(to.path) && isLoggedIn) {
    return next("/home");
  }

  // Allow landlords to access landlord pages only
  if (landlordPages.includes(to.path) && userRole !== "landlord") {
    toast.error("You do not have permission to access this page.");
    return next("/home");
  }

  // Allow tenants to access tenant pages only
  if (tenantPages.includes(to.path) && userRole !== "tenant") {
    toast.error("You do not have permission to access this page.");
    return next("/landlord");
  }

  next();
});

// Workaround for https://github.com/vitejs/vite/issues/11804
router.onError((err, to) => {
  if (err?.message?.includes?.('Failed to fetch dynamically imported module')) {
    if (!localStorage.getItem('vuetify:dynamic-reload')) {
      console.log('Reloading page to fix dynamic import error')
      localStorage.setItem('vuetify:dynamic-reload', 'true')
      location.assign(to.fullPath)
    } else {
      console.error('Dynamic import error, reloading page did not fix it', err)
    }
  } else {
    console.error(err)
  }
})

router.isReady().then(() => {
  localStorage.removeItem('vuetify:dynamic-reload')
})

export default router
