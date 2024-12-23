<template>
    <v-container>
        <v-row align="center" justify="center">
            <v-col cols="12" sm="12" md="6">
                <div class="input-wrapper">
                    <input type="text" v-model="preferences.subject" placeholder="Subject" class="input" />
                    <input type="number" v-model="preferences.max_price" placeholder="Max Price" class="input" />
                    <input type="number" v-model="preferences.min_size" placeholder="Min Size" class="input" />
                    <input type="text" v-model="preferences.preferred_location" placeholder="Preferred Location" class="input" />
                    <input
                        type="text"
                        v-model="preferences.required_amenities"
                        placeholder="Required Amenities (comma separated)"
                        class="input"
                    />
                </div>
            </v-col>
            <v-col cols="12" sm="4" md="6">
                <v-slider
                    v-model="preferences.safety_weight"
                    :min="0"
                    :max="1"
                    :step="0.1"
                    thumb-label="always"
                    color="blue-lighten-2"
                    label="Safety Weight"
                    class="slider"
                ></v-slider>

                <v-slider
                    v-model="preferences.cleanliness_weight"
                    :min="0"
                    :max="1"
                    :step="0.1"
                    thumb-label="always"
                    color="blue-lighten-2"
                    label="Cleanliness Weight"
                    class="slider"
                ></v-slider>

                <v-slider
                    v-model="preferences.accessibility_weight"
                    :min="0"
                    :max="1"
                    :step="0.1"
                    thumb-label="always"
                    color="blue-lighten-2"
                    label="Accessibility Weight"
                    class="slider"
                ></v-slider>

                <v-slider
                    v-model="preferences.noise_level_weight"
                    :min="0"
                    :max="1"
                    :step="0.1"
                    color="blue-lighten-2"
                    thumb-label="always"
                    label="Noise Level Weight"
                    class="slider"
                ></v-slider>
                <v-btn color="blue-lighten-2" @click="submitPreferences" block>Submit Preferences</v-btn>
            </v-col>
        </v-row>
        <br />
    </v-container>
    <v-dialog v-model="showDialog" max-width="600px">
        <v-card class="bg-card2">
            <v-card-title>Room Suggestions</v-card-title>
            <v-card-text>
                <div v-if="filteredRooms.length > 0" v-for="room in filteredRooms" :key="room.id">
                    <v-img src="@/assets/images/room.jpeg" alt="Room Image" ></v-img>
                  
                    <p class="mt-5"><strong><v-icon>mdi-book</v-icon>Description:</strong> {{ room.description }}</p>
                    <p><strong><v-icon>mdi-map</v-icon>Location:</strong> {{ room.location }}</p>
                    <p><strong><v-icon>mdi-star</v-icon>Amenities:</strong> {{ room.amenities.join(', ') }}</p> <!-- Join amenities list -->
                    <p><strong><v-icon>mdi-check</v-icon>Availability:</strong> {{ room.availability }}</p>
                    <p><strong><v-icon>mdi-shield-check</v-icon>Safety Score:</strong> {{ room.safety_score }}</p>
                    <p><strong><v-icon>mdi-graph</v-icon>Cleanliness Score:</strong> {{ room.cleanliness_score }}</p>
                    <p><strong><v-icon>mdi-headphones</v-icon>Accessibility Score:</strong> {{ room.accessibility_score }}</p>
                    <p><strong><v-icon>mdi-headphones</v-icon>Noise Level:</strong> {{ room.noise_level }}</p>
                    <p><strong><v-icon>mdi-currency-php</v-icon>Price:</strong> ${{ room.price }}</p>
                </div>
                <div v-else>
                    <p>No room suggestions available at the moment.</p>
                </div>
            </v-card-text>
            <v-card-actions>
                <v-btn @click="showDialog = false">Close</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import { useToast } from 'vue-toastification';

const toast = useToast();
const preferences = ref({
    subject: 'Tenant Preferences Update',
    max_price: 1500,
    min_size: 25,
    preferred_location: 'Downtown',
    required_amenities: '',
    safety_weight: 0.3,
    cleanliness_weight: 0.3,
    accessibility_weight: 0.2,
    noise_level_weight: 0.2
});

const roomSuggestions = ref([]);

// Define the Room interface to include all relevant properties
interface Room {
    id: number;
    description: string;
    price: number;
    location: string;
    amenities: string[];
    availability: string;
    safety_score: number;
    cleanliness_score: number;
    accessibility_score: number;
    noise_level: number;
}

const filteredRooms = ref<Room[]>([]);
const showDialog = ref(false);

async function submitPreferences() {
    const token = localStorage.getItem('access_token');
    if (!token) {
        console.error('No access token found. Please log in.');
        return;
    }

    const payload = {
        ...preferences.value,
        required_amenities: preferences.value.required_amenities.split(',').map(item => item.trim())
    };

    try {
        // Submit tenant preferences
        const response = await fetch('http://127.0.0.1:5000/tenant/preferences', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(payload)
        });
        const data = await response.json();
        console.log('Preferences submitted successfully:', data);

        // Fetch room suggestions
        const searchResponse = await fetch('http://127.0.0.1:5000/tenant/search', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        const searchData = await searchResponse.json();

        if (searchData.length === 0) {
            // Show a toast warning if no rooms found
            toast.warning('No rooms found');
            return;  // Stop further execution
        }

        roomSuggestions.value = searchData;

        // Fetch details for each room by ID
        const roomDetailsPromises = searchData.map(async (room: any) => {
            try {
                const roomResponse = await fetch(`http://127.0.0.1:5000/landlord/rooms/${room.id}`, {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                const roomData = await roomResponse.json();
                console.log(`Room details for room ${room.id}:`, roomData);
                return roomData;  // Return the detailed room data
            } catch (error) {
                console.error(`Error fetching room ${room.id}:`, error);
                return null;  // Return null if an error occurs for a specific room
            }
        });

        // Wait for all room detail requests to complete
        const filteredRoomsData = await Promise.all(roomDetailsPromises);
        // Filter out null values in case of errors
        filteredRooms.value = filteredRoomsData.filter(room => room !== null);
        console.log('Filtered landlord rooms:', filteredRooms.value);
        showDialog.value = true;

    } catch (error) {
       toast.warning('No rooms found');
    }
}
</script>

<style scoped>
.input-wrapper input {
    background: rgba(232, 250, 255, 0.76);
    border: 2px solid #00b7ff;
    padding: 1rem;
    font-size: 1rem;
    width: 30rem;
    border-radius: 1rem;
    box-shadow: 0 0.4rem rgba(232, 250, 255, 0.096);
    cursor: pointer;
    margin-bottom: 0.5rem;
}

.input-wrapper input:focus {
    outline-color: #00b7ff;
}

.slider {
    margin-bottom: 1rem;
}

@media (max-width: 768px) {
    .input-wrapper input {
        width: 20em;
    }
}.bg-card2 {
  background: rgba(232, 250, 255, 0.76);
  border-radius: 16px;
  box-shadow: 0 4px 10px rgba(79, 204, 254, 0.3);
  backdrop-filter: blur(5px);
  -webkit-backdrop-filter: blur(5px);
  border: 1px solid #64B5F6;
}
</style>
