<template>
    <v-lazy :min-height="200" :options="{ 'threshold': 0.5 }" transition="fade-transition">
        <div id="lander">
            <v-container fluid>
                <v-row>
                    <v-col cols="6" lg="2" sm="6" v-for="room in roomsStore.paginatedRooms" :key="room.id">
                        <div class="text-center">
                            <div class="room-circle" @click="roomsStore.openDialog(room)">
                                <img :src="room.img" alt="Room Image" class="rounded-circle room-image">
                            </div>
                        </div>
                    </v-col>
                </v-row>
                <br> <br>

                <v-pagination v-model="roomsStore.currentPage" :length="roomsStore.totalPages"></v-pagination>
                <v-divider></v-divider>
            </v-container>

            <v-dialog v-model="roomsStore.dialog" max-width="500px">
                <v-card>
                    <v-card-title class="text-center">{{ roomsStore.selectedRoom?.title }}</v-card-title>
                    <v-card-text>
                        <v-img :src="roomsStore.selectedRoom?.img" alt="Room Image"></v-img>
                        <p class="mt-5"><strong><v-icon class="me-2">mdi-book</v-icon>Description:</strong> {{
                            roomsStore.selectedRoom?.description }}</p>
                        <p><strong><v-icon class="me-2">mdi-calendar</v-icon>Created At:</strong> {{
                            roomsStore.selectedRoom?.created_at }}</p>
                        <p><strong><v-icon class="me-2">mdi-account-group</v-icon>Maximum Pax:</strong> {{
                            roomsStore.selectedRoom?.maximum_pax }}</p>
                        <!-- Add more room details here -->
                    </v-card-text>
                    <v-card-actions>
                        <v-btn color="primary" @click="roomsStore.dialog = false">Close</v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>
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