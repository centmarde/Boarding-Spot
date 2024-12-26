<template>
    <v-lazy :min-height="200" :options="{ 'threshold': 0.5 }" transition="fade-transition">
        <div id="card-rooms">

            <v-container>
                <v-row>
                    <v-col cols="12" md="4" v-for="room in roomsStore.paginatedRooms" :key="room.id">
                        <v-card elevation="8" class="pa-10 bg-card" color="">
                            <v-img src="@/assets/images/room.jpeg" alt="Room Image"></v-img>
                            <v-card-title>{{ room.title }}</v-card-title>
                            <v-card-text>
                                <p><strong>Description:</strong> {{ room.description }}</p>
                                <p><strong>Availability:</strong> {{ room.availability ? 'Yes' : 'No' }}</p>
                                <p><strong>Price:</strong> {{ room.price }}</p>
                                <p><strong>Location:</strong> {{ room.location }}</p>
                            </v-card-text>
                            <v-card-actions>
                                <v-row class=" mx-auto">
                                    <v-col cols="12" md="6"> <BookRoomButton/></v-col>
                                    <v-col cols="12" md="6"> <v-btn color="primary" @click="roomsStore.openDialog(room)">More Info..</v-btn></v-col>
                                </v-row>
                            </v-card-actions>
                        </v-card>
                    </v-col>
                </v-row>
                <br><br>
                <v-pagination class="text-light" v-model="roomsStore.currentPage" :length="roomsStore.totalPages"></v-pagination>
            </v-container>

            <v-dialog v-model="roomsStore.dialog" max-width="500px">
                <v-card class="bg-card2">
                    <v-card-title class="text-center">{{ roomsStore.selectedRoom?.title }}</v-card-title>
                    <v-card-text>
                        <v-img :src="roomsStore.selectedRoom?.img" alt="Room Image"></v-img>
                        <p class="mt-5"><strong><v-icon class="me-2">mdi-book</v-icon>Description:</strong> {{ roomsStore.selectedRoom?.description }}</p>
                        <p><strong><v-icon class="me-2">mdi-diamond</v-icon>Amenities:</strong> {{ roomsStore.selectedRoom?.amenities }}</p>
                        <p><strong><v-icon class="me-2">mdi-ruler</v-icon>Room Dimensions:</strong> {{ roomsStore.selectedRoom?.size }}</p>
                        <p><strong><v-icon class="me-2">mdi-currency-usd</v-icon>Price:</strong> {{ roomsStore.selectedRoom?.price }}</p>
                        <p><strong><v-icon class="me-2">mdi-map-marker</v-icon>Location:</strong> {{ roomsStore.selectedRoom?.location }}</p>
  
                    </v-card-text>
                    <v-card-actions>
                        <BookRoomButton/>
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
import BookRoomButton from './BookRoomButton.vue';
import { useToast } from 'vue-toastification';

// Define emits
const emit = defineEmits();

const roomsStore = useRoomStore();
const toast = useToast();

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

.bg-card {
  background: rgba(161, 205, 247, 0.15);
  border-radius: 16px;
  box-shadow: 0 4px 10px rgba(79, 204, 254, 0.3);
  backdrop-filter: blur(5px);
  -webkit-backdrop-filter: blur(5px);
  border: 1px solid #64B5F6;
}
</style>
