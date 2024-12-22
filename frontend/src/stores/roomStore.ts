   // src/stores/roomStore.ts
   import { defineStore } from 'pinia';
   import { ref, computed } from 'vue';
   import { supabase } from '@/lib/supabase';

   interface Room {
     landlord_id: number | null;
     title: string;
     description: string;
     price: number | null;
     size: string | null;
     location: string;
     amenities: string;
     safety_score: number;
     cleanliness_score: number;
     accessibility_score: number;
     noise_level: number;
   }

   export const useRoomStore = defineStore('roomStore', () => {
     const rooms = ref<Room[]>([]);
     const dialog = ref(false);
     const selectedRoom = ref<Room | null>(null);
     const currentPage = ref(1);
     const itemsPerPage = 6;

     const paginatedRooms = computed(() => {
       const start = (currentPage.value - 1) * itemsPerPage;
       const end = start + itemsPerPage;
       return rooms.value.slice(start, end);
     });

     const totalPages = computed(() => Math.ceil(rooms.value.length / itemsPerPage));

     async function fetchRooms() {
       const { data, error } = await supabase
         .from('rooms')
         .select('*');

       if (error) {
         console.error('Error fetching rooms:', error);
       } else {
         rooms.value = data as Room[];
       }
     }

     function openDialog(room: Room) {
       selectedRoom.value = room;
       dialog.value = true;
     }

     async function fetchRandomRoom() {
       const { data, error } = await supabase
         .from('rooms')
         .select('*');

       if (error) {
         console.error('Error fetching rooms:', error);
       } else if (data.length > 0) {
         rooms.value = data.sort(() => Math.random() - 0.5) as Room[];
       }
     }

     return {
       rooms,
       dialog,
       selectedRoom,
       currentPage,
       paginatedRooms,
       totalPages,
       fetchRooms,
       openDialog,
       fetchRandomRoom,
     };
   });