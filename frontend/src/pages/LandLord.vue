<template>
  <LayoutWrapper>
    <template #content>
      <v-container fluid>
        <v-card class="pa-10" max-width="100%" elevation="16">
          <div v-if="roomStore.rooms.length">
            <h2>Rooms</h2>
            <v-data-table
              :items="roomStore.rooms"
              item-key="id"
              class="elevation-1"
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
        </v-card>
      </v-container>
    </template>
  </LayoutWrapper>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { useRoomStore } from '../stores/roomStore';
import LayoutWrapper from '../layouts/LayoutWrapper.vue';

const roomStore = useRoomStore();

onMounted(async () => {
  await roomStore.fetchRooms();
});
</script>

<style scoped>
</style>
  