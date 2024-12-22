<template>
  <LayoutWrapper>
    <template #content>
      <v-container fluid>
      <v-card class="pa-10 " max-width="100%" elevation="16">
        

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
                <th class="text-left">Description</th>
                <th class="text-left">Image</th>
                <th class="text-left">Price</th>
                <th class="text-left">Max Pax</th>
                <th class="text-left">Bed Count</th>
                <th class="text-left">Appliances</th>
                <th class="text-left">AC</th>
                <th class="text-left">TV</th>
                <th class="text-left">Dimensions</th>
                <th class="text-left">Internet</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in roomStore.rooms" :key="item.id">
                <td>{{ item.title }}</td>
                <td>{{ item.description }}</td>
                <td>
                  <img :src="item.img" alt="Room Image" style="width: 100px; height: auto;" />
                </td>
                <td>{{ item.price }}</td>
                <td>{{ item.maximum_pax }}</td>
                <td>{{ item.bed_count }}</td>
                <td>{{ item.appliances }}</td>
                <td>{{ item.AC }}</td>
                <td>{{ item.TV }}</td>
                <td>{{ item.room_dimensions }}</td>
                <td>{{ item.internet }}</td>
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
  