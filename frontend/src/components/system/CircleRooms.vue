<template>
    <v-lazy :min-height="200" :options="{ 'threshold': 0.5 }" transition="fade-transition">
        <div id="lander">
            <v-container fluid>
                <v-row>
                    <v-col cols="6" lg="2" sm="6" v-for="room in roomsStore.paginatedRooms" :key="room.id">
                        <div class="text-center">
                            <v-tooltip  location="bottom" :text="`${room.title} - $${room.price}`">
                                <template v-slot:activator="{ props }">
                                    <div class="room-circle" v-bind="props" @click="roomsStore.openDialog(room)">
                                        <img :src="room.image_url" alt="Room Image" class="rounded-circle room-image">
                                    </div>
                                </template>
                            </v-tooltip>
                        </div>
                    </v-col>
                </v-row>
                <br> <br>

                <v-pagination v-model="roomsStore.currentPage" :length="roomsStore.totalPages"></v-pagination>
                <v-divider></v-divider>
            </v-container>

          
        </div>
    </v-lazy>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { useRoomStore } from '@/stores/roomStore';

const roomsStore = useRoomStore();

onMounted(() => {
    roomsStore.fetchRooms();
});
</script>

<style scoped>
.room-circle {
    background-color: var(--v-surface-variant);
    border-radius: 50%;
    height: 200px;
    width: 200px;
    margin: 0 auto;
    transition: box-shadow 0.3s ease;
    cursor: pointer;
}

.room-circle:hover {
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.room-image {
    height: 200px;
    width: 200px;
    border-radius: 50%;
}

/* Media query for small screens */
@media (max-width: 600px) {

    .room-circle,
    .room-image {
        height: 100px;
        /* Half of 200px */
        width: 100px;
        /* Half of 200px */
    }
}
</style>