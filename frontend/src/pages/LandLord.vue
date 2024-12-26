<template>
  <LayoutWrapper>
    <template #content>
      <v-container fluid>
        <div class="pa-10" max-width="100%" elevation="16">
          <div class="bg-card pa-10" v-if="roomStore.rooms.length">
            <h2 class="text-center mb-10">Rooms</h2>
            <v-table>
              <thead>
                <tr>
                  <th class="text-left">Name</th>
                  <th class="text-left">Created At</th>
                  <th class="text-left">Description</th>
                  <th class="text-left">Image</th>
                  <th class="text-left">Price</th>
                  <th class="text-left">Amenities</th>
                  <th class="text-left">Size</th>
                  <th class="text-left">Availability</th>
                  <th class="text-left">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in paginatedRooms" :key="item.id">
                  <td>{{ item.title }}</td>
                  <td>{{ item.created_at }}</td>
                  <td>{{ item.description }}</td>
                  <td>
                    <img
                     :src="item.image_url"
                      alt="Room Image"
                      style="width: 100px; height: auto;"
                    />
                  </td>
                  <td>{{ item.price }}</td>
                  <td>{{ Array.isArray(item.amenities) ? item.amenities.join(', ') : item.amenities }}</td>
                  <td>{{ item.size }}</td>
                  <td>{{ item.availability ? 'Yes' : 'No' }}</td>
                  <td>
                    <v-btn color="primary" @click="openEditForm(item)">Edit</v-btn>
                  </td>
                </tr>
              </tbody>
            </v-table>

            <!-- Pagination -->
            <v-pagination
              v-if="totalPages > 1"
              v-model="currentPage"
              :length="totalPages"
              :total-visible="5"
              @input="fetchRooms"
            />
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
              <v-img 
                :src="currentRoom.image_url" 
                alt="Room Image" 
                @click="openImageUploadDialog" 
                style="cursor: pointer;"
              ></v-img>
              <v-text-field v-model="currentRoom.title" label="Room Title" required></v-text-field>
              <v-textarea v-model="currentRoom.description" label="Description" required></v-textarea>
              <v-text-field v-model="currentRoom.price" label="Price" type="number" required></v-text-field>
              <v-textarea v-model="currentRoom.amenities" label="Amenities (comma separated)" required></v-textarea>
              <v-text-field v-model="currentRoom.size" label="Size" type="number" required></v-text-field>
              <v-switch v-model="currentRoom.availability" label="Availability"></v-switch>
              <v-text-field v-model="currentRoom.accessibility_score" label="Accessibility Score" type="number" step="0.1" required></v-text-field>
              <v-text-field v-model="currentRoom.cleanliness_score" label="Cleanliness Score" type="number" step="0.1" required></v-text-field>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-btn color="red" @click="editDialog = false">Cancel</v-btn>
            <v-btn color="green" @click="submitEditRoom" :disabled="!valid">Save</v-btn>
          </v-card-actions>

          <!-- New Image Upload Dialog -->
          <v-dialog v-model="imageUploadDialog" max-width="500px">
            <v-card>
              <v-card-title>Upload Room Image</v-card-title>
              <v-card-text>
                <v-file-input v-model="newImage" label="Select Image" accept="image/*" />
              </v-card-text>
              <v-card-actions>
                <v-btn color="red" @click="imageUploadDialog = false">Cancel</v-btn>
                <v-btn color="green" @click="submitImageUpload" :disabled="!newImage">Upload</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-card>
      </v-dialog>
    </template>
  </LayoutWrapper>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, defineEmits, onBeforeUnmount } from 'vue';
import { useRoomStore } from '../stores/roomStore';
import LayoutWrapper from '../layouts/LayoutWrapper.vue';
import AddRooms from '../components/system/AddRooms.vue';
import { useToast } from 'vue-toastification';
import { supabase } from '../lib/supabase';

const roomStore = useRoomStore();
const toast = useToast();
const editDialog = ref(false);
const currentRoom = ref<any>({});
const valid = ref(true);
const itemsPerPage = 5;
const currentPage = ref(1);
const imageUploadDialog = ref(false);
const newImage = ref<File | null>(null);

// Computed property to return the paginated rooms
const paginatedRooms = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return roomStore.rooms.slice(start, end);
});

// Computed property for the total number of pages
const totalPages = computed(() => {
  return Math.ceil(roomStore.rooms.length / itemsPerPage);
});

// Fetch rooms with pagination logic
const fetchRooms = async () => {
  const token = localStorage.getItem('access_token');
  if (!token) return;

  await roomStore.fetchRooms();
};

onMounted(fetchRooms);

// Open the edit form with the selected room data
const openEditForm = (room: any) => {
  currentRoom.value = { ...room };
  editDialog.value = true;
};

// Submit the edited room data
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
      },
      body: JSON.stringify(roomData),
    });

    if (!response.ok) {
      throw new Error(`Error updating room: ${response.statusText}`);
    }

    roomStore.fetchRooms();
    editDialog.value = false;
  } catch (error) {
    console.error('Error updating room:', error);
  }
};

// Function to open the image upload dialog
const openImageUploadDialog = () => {
  imageUploadDialog.value = true;
};

// Function to handle image upload
const submitImageUpload = async () => {
  const token = localStorage.getItem('access_token');
  if (!token || !newImage.value) return;

  const formData = new FormData();
  formData.append('image', newImage.value);

  // Define the file variable from newImage
  const file = newImage.value;
  const fileName = `blob/${Date.now()}_${file.name}`; // Use the defined file variable

  try {
    // Upload image to Supabase
    const { data, error } = await supabase
      .storage
      .from('rooms')
      .upload(fileName, file, {
        cacheControl: "3600",
        upsert: true,
      });

    if (error) throw error;

    // Generate the public URL for the uploaded image
    const imageUrl = supabase
      .storage
      .from('rooms')
      .getPublicUrl(fileName).data.publicUrl;

    // Pass the image URL to your current room object
    currentRoom.value.image_url = imageUrl;
    console.log('Image uploaded successfully:', imageUrl);

    // Now, send the URL to your Flask API
    const response = await fetch(`http://127.0.0.1:5000/landlord/rooms/${currentRoom.value.id}/upload-image`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        image_url: imageUrl,  // Send the URL as part of the request body
      }),
    });

    if (!response.ok) {
      throw new Error(`Error uploading image: ${response.statusText}`);
    }

    // Close the image upload dialog and reset the form
    imageUploadDialog.value = false;
    newImage.value = null; // Reset the file input
  } catch (error) {
    console.error('Error uploading image:', error);
    alert('Failed to upload image.');
  }
};


// Subscribe to Supabase changes
const channels = supabase.channel('custom-all-channel')
  .on(
    'postgres_changes',
    { event: '*', schema: 'public', table: 'rooms' },
    (payload) => {
      if (payload.eventType === 'INSERT') {
        toast.success('A room has been booked!');
      }
    }
  )
  .subscribe();

onBeforeUnmount(() => {
  supabase.removeChannel(channels); // Clean up the subscription on component unmount
});

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
