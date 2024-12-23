//if supabase is applied use here

import { createClient } from '@supabase/supabase-js';
import { useToast } from 'vue-toastification';
import { useRouter } from 'vue-router';

const toast = useToast();
const router = useRouter();
// const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
// const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY;

// export const supabase = createClient(supabaseUrl, supabaseAnonKey);

export async function doLogout() {
    // Confirm logout
    const confirmed = window.confirm("Are you sure you want to logout?");
  
    // If not confirmed, exit the function early
    if (!confirmed) {
      return;
    }
    // Supabase Logout
    // const { error } = await supabase.auth.signOut();
  
   else {
      toast("Logout Successfully!"); // Notify successful logout
      localStorage.clear(); // Clear local storage
    //   router.push('/');
    window.location.href = '/';
    }
}