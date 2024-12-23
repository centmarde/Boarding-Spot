<template>
  <LayoutWrapper>
    <template #content>
      <v-container fluid>
        <div class="pa-10" max-width="100%" elevation="16">
          <div class="bg-card pa-10" v-if="roomStore.rooms.length">
            <h2 class="text-center mb-10">Rooms</h2>
            <v-data-table
              :items="roomStore.rooms" 
              item-key="id"
              class="elevation-1"
              :items-per-page="itemsPerPage"
              :headers="tableHeaders"
            >
              <template v-slot:item.image="{ item }">
                <img src="`@/assets/images/room.jpeg`" alt="Room Image" style="width: 100px; height: auto;" />
              </template>

              <template v-slot:item.amenities="{ item }">
                {{ Array.isArray(item.amenities) ? item.amenities.join(', ') : item.amenities }}
              </template>

              <template v-slot:item.availability="{ item }">
                {{ item.availability ? 'Yes' : 'No' }}
              </template>

              <template v-slot:item.actions="{ item }">
                <v-btn color="primary" @click="openEditForm(item)">Edit</v-btn>
              </template>
            </v-data-table>
          </div>
          <div v-else>
            <p>No rooms available.</p>
          </div>
          <v-divider class="my-10"></v-divider>
          <AddRooms />
        </div>
      </v-container>
      
      <!-- Edit Room Form Modal -->
      <v-dialog v-model="editDialog" max-width="500px">
        <v-card>
          <v-card-title>Edit Room</v-card-title>
          <v-card-text>
            <v-form ref="editForm" v-model="valid" lazy-validation>
              <v-text-field v-model="currentRoom.title" label="Room Title" required></v-text-field>
              <v-textarea v-model="currentRoom.description" label="Description" required></v-textarea>
              <v-text-field v-model="currentRoom.price" label="Price" type="number" required></v-text-field>
              <v-textarea v-model="currentRoom.amenities" label="Amenities (comma separated)" required></v-textarea>
              <v-text-field v-model="currentRoom.size" label="Size" type="number" required></v-text-field>
              <v-switch v-model="currentRoom.availability" label="Availability" ></v-switch>
              <v-text-field v-model="currentRoom.accessibility_score" label="Accessibility Score" type="number" step="0.1" required></v-text-field>
              <v-text-field v-model="currentRoom.cleanliness_score" label="Cleanliness Score" type="number" step="0.1" required></v-text-field>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-btn color="red" @click="editDialog = false">Cancel</v-btn>
            <v-btn color="green" @click="submitEditRoom" :disabled="!valid">Save</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      
    </template>
  </LayoutWrapper>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRoomStore } from '../stores/roomStore';
import LayoutWrapper from '../layouts/LayoutWrapper.vue';
import AddRooms from '../components/system/AddRooms.vue';

const roomStore = useRoomStore();
const editDialog = ref(false);  // Control the modal visibility
const currentRoom = ref<any>({});  // The room currently being edited
const valid = ref(true);  // Form validation state
const itemsPerPage = ref(10);  // Set the items per page limit

const fetchRoomsPeriodically = async () => {
  await roomStore.fetchRooms();
  setTimeout(fetchRoomsPeriodically, 3000);
};

onMounted(fetchRoomsPeriodically);

const tableHeaders = [
  { text: 'Name', align: 'start' as 'start', key: 'title' },
  { text: 'Created At', align: 'start' as 'start', key: 'created_at' },
  { text: 'Description', align: 'start' as 'start', key: 'description' },
  { text: 'Image', align: 'start' as 'start', key: 'image' },
  { text: 'Price', align: 'start' as 'start', key: 'price' },
  { text: 'Amenities', align: 'start' as 'start', key: 'amenities' },
  { text: 'Size', align: 'start' as 'start', key: 'size' },
  { text: 'Availability', align: 'start' as 'start', key: 'availability' },
  { text: 'Actions', align: 'start' as 'start', key: 'actions' }
];

const openEditForm = (room: any) => {
  currentRoom.value = { ...room };
  editDialog.value = true;
};

const submitEditRoom = async () => {
  const token = localStorage.getItem('access_token');
  if (!token) return;

  const roomId = currentRoom.value.id;
  const roomData = currentRoom.value;

  try {
    const response = await fetch(`http://127.0.0.1:5000/landlord/rooms/${roomId}`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
        mode: 'no-cors',
      },
      body: JSON.stringify(roomData) 
    });

    if (!response.ok) {
      throw new Error(`Error updating room: ${response.statusText}`);
    }

    roomStore.fetchRooms(); // Re-fetch rooms after updating
    editDialog.value = false; // Close the modal
  } catch (error) {
    console.error('Error updating room:', error);
  }
};
</script>

<style scoped>
.bg-card {
  background: rgba(161, 205, 247, 0.15);
  border-radius: 16px;
  box-shadow: 0 4px 10px rgba(79, 204, 254, 0.3);
  backdrop-filter: blur(5px);
  -webkit-backdrop-filter: blur(5px);
  border: 1px solid #64B5F6;
}
</style>
