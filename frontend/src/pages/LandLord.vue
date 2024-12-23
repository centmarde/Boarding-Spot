<template>
  <LayoutWrapper>
    <template #content>
      <v-container fluid>
        <div class="pa-10 " max-width="100%" elevation="16">
          <AddRooms />
          <v-divider class="my-10"></v-divider>
          <div class="bg-card" v-if="roomStore.rooms.length">
            <h2 class="text-center my-2">Rooms</h2>
            <v-data-table
              :items="roomStore.rooms"
              item-key="id"
              class="elevation-1 "
            >
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
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in roomStore.rooms" :key="item.id">
                  <td>{{ item.title }}</td>
                  <td>{{ item.created_at }}</td>
                  <td>{{ item.description }}</td>
                  <td>
                    <img src="@/assets/images/room.jpeg" alt="Room Image" style="width: 100px; height: auto;" />
                  </td>
                  <td>{{ item.price }}</td>
                 
                  <td>
                    {{ Array.isArray(item.amenities) ? item.amenities.join(', ') : item.amenities }}
                  </td>
                  <td>{{ item.size }}</td>
                  <td>{{ item.availability ? 'Yes' : 'No' }}</td>
                </tr>
              </tbody>
            </v-data-table>
          </div>
          <div v-else>
            <p>No rooms available.</p>
          </div>
        </div>
      </v-container>
    </template>
  </LayoutWrapper>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { useRoomStore } from '../stores/roomStore';
import LayoutWrapper from '../layouts/LayoutWrapper.vue';
import AddRooms from '../components/system/AddRooms.vue';

const roomStore = useRoomStore();

onMounted(async () => {
  await roomStore.fetchRooms();
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
  