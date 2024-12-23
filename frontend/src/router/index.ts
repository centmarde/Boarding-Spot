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

// Token check interval every 5 seconds
setInterval(() => {
  const token = localStorage.getItem('access_token');
  const currentPath = router.currentRoute.value.path; // Get current route path
  
  if (token === null && currentPath !== '/') {
    toast.error('Your session has expired.');
    router.push('/');
  }
}, 5000);

router.beforeEach((to, from, next) => {
  const isLoggedIn = localStorage.getItem("access_token") !== null;
  console.log(isLoggedIn);
  const authUserStore = useAuthUserStore();
  const userRole = localStorage.getItem("user_type");
  console.log(userRole);

  const publicPages = ["/"];
  const landlordPages = ["/landlord"];
  const tenantPages = ["/home"];

  if (to.meta.requiresAuth && !isLoggedIn) {
    return next("/");
  }

  if (publicPages.includes(to.path) && isLoggedIn) {
    return next("/home");
  }

  if (landlordPages.includes(to.path) && userRole !== "landlord") {
    toast.error("You do not have permission to access this page.");
    return next("/home");
  }

  if (tenantPages.includes(to.path) && userRole !== "tenant") {
    return next("/landlord");
  }

  next();
});

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
