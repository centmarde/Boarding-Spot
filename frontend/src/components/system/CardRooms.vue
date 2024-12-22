<template>
    <v-lazy :min-height="200" :options="{ 'threshold': 0.5 }" transition="fade-transition">
        <div id="card-rooms">

            <v-container>
                <v-row>
                    <v-col cols="12" md="4" v-for="room in roomsStore.paginatedRooms" :key="room.id">
                        <v-card elevation="8" class="pa-10">
                            <v-img :src="room.img" alt="Room Image"></v-img>
                            <v-card-title>{{ room.title }}</v-card-title>
                            <v-card-text>
                                <p><strong>Description:</strong> {{ room.description }}</p>
                                <p><strong>Created At:</strong> {{ room.created_at }}</p>
                                <p><strong>Maximum Pax:</strong> {{ room.maximum_pax }}</p>
                            </v-card-text>
                            <v-card-actions>
                                <v-btn color="primary" @click="roomsStore.openDialog(room)">More Information</v-btn>
                            </v-card-actions>
                        </v-card>
                    </v-col>
                </v-row>
                <br> <br>
                <v-pagination class="text-light" v-model="roomsStore.currentPage" :length="roomsStore.totalPages"></v-pagination>
            </v-container>

            <v-dialog v-model="roomsStore.dialog" max-width="500px">
                <v-card>
                    <v-card-title class="text-center">{{ roomsStore.selectedRoom?.title }}</v-card-title>
                    <v-card-text>
                        <v-img :src="roomsStore.selectedRoom?.img" alt="Room Image"></v-img>
                        <p class="mt-5"><strong><v-icon class="me-2">mdi-book</v-icon>Description:</strong> {{ roomsStore.selectedRoom?.description }}</p>
                        <p><strong><v-icon class="me-2">mdi-calendar</v-icon>Created At:</strong> {{ roomsStore.selectedRoom?.created_at }}</p>
                        <p><strong><v-icon class="me-2">mdi-account</v-icon>Maximum Pax:</strong> {{ roomsStore.selectedRoom?.maximum_pax }}</p>
                        <p><strong><v-icon class="me-2">mdi-television</v-icon>TV:</strong> {{ roomsStore.selectedRoom?.TV }}</p>
                        <p><strong><v-icon class="me-2">mdi-air-conditioner</v-icon>AC:</strong> {{ roomsStore.selectedRoom?.AC }}</p>
                        <p><strong><v-icon class="me-2">mdi-wifi</v-icon>Internet:</strong> {{ roomsStore.selectedRoom?.internet }}</p>
                        <p><strong><v-icon class="me-2">mdi-ruler</v-icon>Room Dimensions:</strong> {{ roomsStore.selectedRoom?.room_dimensions }}</p>
                        <p><strong><v-icon class="me-2">mdi-currency-php</v-icon>Price PHP:</strong> {{ roomsStore.selectedRoom?.price }}</p>

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
  roomsStore.fetchRandomRoom();
});


</script>

<style scoped>

.card-image {
    height: 200px;
    width: 100%;
    object-fit: cover;
}

/* Media query for small screens */
@media (max-width: 600px) {
    .card-image {
        height: 100px; /* Adjusted for smaller screens */
    }
}
</style>
