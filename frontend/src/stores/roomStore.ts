// src/stores/roomStore.ts
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { useToast } from 'vue-toastification';

interface Room {
  id: string;
  img: string;
  created_at: string;
  maximum_pax: number;
  landlord_id: number | null;
  title: string;
  description: string;
  price: number | null;
  size: string | null;
  location: string;
  amenities: string[];
  safety_score: number;
  cleanliness_score: number;
  accessibility_score: number;
  noise_level: number;
  availability: boolean;
}

export const useRoomStore = defineStore('roomStore', () => {
  const toast = useToast();
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
    try {
      const response = await fetch('http://127.0.0.1:5000/landlord/rooms');
      if (!response.ok) {
        throw new Error(`Error fetching rooms: ${response.statusText}`);
      }
      const data = await response.json();
  

      rooms.value = data.map((room: any) => ({
        ...room,
        amenities: room.amenities.join(', '),
      })) as Room[];

     
    } catch (error) {
      console.error('Error fetching rooms:', error);
    }
  }

  function openDialog(room: Room) {
    selectedRoom.value = room;
    dialog.value = true;
  }

  async function fetchRandomRoom() {
    try {
      const response = await fetch('http://127.0.0.1:5000/landlord/rooms');
      if (!response.ok) {
        throw new Error(`Error fetching rooms: ${response.statusText}`);
      }
      const data = await response.json();
      if (data.length > 0) {
        rooms.value = data.sort(() => Math.random() - 0.5) as Room[];
      }
    } catch (error) {
      console.error('Error fetching rooms:', error);
    }
  }

  async function createRoom(newRoom: Omit<Room, 'id' | 'created_at' | 'availability'>) {
    const token = localStorage.getItem('access_token');
    try {
      const response = await fetch('http://127.0.0.1:5000/landlord/rooms', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`, 
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newRoom),
      });
      if (!token) {
        console.error("No access token found.");
        return;
      }
      
      if (!response.ok) {
        throw new Error(`Error creating room: ${response.statusText}`);
      }
      const createdRoom = await response.json();
      rooms.value.push(createdRoom);
    } catch (error) {
      console.error('Error creating room:', error);
    }
  }


  function showToast(message: string) {
    toast.success(message);
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
    createRoom,
    showToast,
  };
});
