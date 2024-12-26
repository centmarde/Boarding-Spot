<template>
    <v-card class="py-5 bg-card">
        <v-container>
    <v-form ref="form" v-model="formValid">
        
        

      <v-row>
       <v-col>
        <v-text-field
            v-model="roomForm.title"
            :rules="[rules.required, rules.maxLength(50)]"
            label="Title"
            required
          
          ></v-text-field>
       </v-col>
       <v-col>
      <v-file-input
        v-model="roomForm.image"
        :rules="[rules.required]"
        label="Upload Image"
        accept="image/*"
        required
      ></v-file-input>
    </v-col>
      </v-row>
      <v-row>
        <v-col>  <v-text-field
        v-model="roomForm.price"
        :rules="[rules.required, rules.positiveNumber]"
        label="Price"
        type="number"
        required
      ></v-text-field></v-col>
        <v-col><v-text-field
        v-model="roomForm.size"
        :rules="[rules.required, rules.maxLength(20)]"
        label="Size (e.g., '50')"
        type="number"
        required
      ></v-text-field></v-col>
      </v-row>
      <v-row>
        <v-col>  <v-text-field
        v-model="roomForm.location"
        :rules="[rules.required, rules.maxLength(100)]"
        label="Location"
        required
      ></v-text-field></v-col>
        <v-col> <v-combobox
        v-model="roomForm.amenities"
        :items="availableAmenities"
        :rules="[rules.required]"
        label="Amenities"
        multiple
        required
      ></v-combobox></v-col>
      </v-row>
    
  <v-row>
    <v-col>
        <v-textarea
            v-model="roomForm.description"
            :rules="[rules.required, rules.maxLength(300)]"
            label="Description"
            rows="6"
            required
          ></v-textarea>
    </v-col>
    <v-col>  <v-slider
        v-model="roomForm.safety_score"
        :min="0"
        :max="10"
        step="1"
        label="Safety Score"
        ticks="always"
      ></v-slider>

      <!-- Cleanliness Score -->
      <v-slider
        v-model="roomForm.cleanliness_score"
        :min="0"
        :max="10"
        step="1"
        label="Cleanliness Score"
        ticks="always"
      ></v-slider>

      <!-- Accessibility Score -->
      <v-slider
        v-model="roomForm.accessibility_score"
        :min="0"
        :max="10"
        step="1"
        label="Accessibility Score"
        ticks="always"
      ></v-slider>

      <!-- Noise Level -->
      <v-slider
        v-model="roomForm.noise_level"
        :min="0"
        :max="10"
        step="1"
        label="Noise Level"
        ticks="always"
      ></v-slider></v-col>
  </v-row>


  <!-- Submit Button -->
  <v-btn style="width: 100%;" :disabled="!formValid" color="primary" @click="submitForm">
    Submit
  </v-btn>
    </v-form>
  </v-container>
    </v-card>
  
</template>

<script>
import { ref } from "vue";
import { useRoomStore } from "@/stores/roomStore";
import {supabase} from "@/lib/supabase"
import { useToast } from 'vue-toastification';

const toast = useToast();

export default {
  setup() {
    const { createRoom } = useRoomStore();

    const roomForm = ref({
      title: "",
      description: "",
      price: null,
      size: "",
      location: "",
      amenities: [],
      safety_score: 0,
      cleanliness_score: 0,
      accessibility_score: 0,
      noise_level: 0,
      image: null,
    });

    const formValid = ref(false);
    const rooms = ref([]);

    const availableAmenities = ref([
      "WiFi",
      "Parking",
      "Pool",
      "Gym",
      "Laundry",
    ]);

    const rules = {
      required: (value) => !!value || "This field is required.",
      maxLength: (length) => (value) =>
        value.length <= length || `Max length is ${length} characters.`,
      positiveNumber: (value) =>
        value > 0 || "The value must be a positive number.",
    };

    const submitForm = async () => {
      try {
        const token = localStorage.getItem('access_token');
        console.log(token);
        if (!token || !roomForm.value.image) return;

        const formData = new FormData();
        formData.append('image', roomForm.value.image);

        const file = roomForm.value.image;
        const fileName = `blob/${Date.now()}_${file.name}`;

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
          roomForm.value.image_url = imageUrl;
          console.log('Image uploaded successfully:', imageUrl);
          toast.success("room uploaded successfully");

         
          const response = await fetch('http://127.0.0.1:5000/landlord/rooms', {
            method: 'POST',
            headers: {
              Authorization: `Bearer ${token}`, 
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ ...roomForm.value, image_url: imageUrl }),
          });

          if (!response.ok) {
            throw new Error(`Error creating room: ${response.statusText}`);
          }
          const createdRoom = await response.json();
          rooms.value.push(createdRoom);


          setTimeout(() => {
        window.location.reload();
      }, 2000); 
        } catch (error) {
          console.error('Error creating room:', error);
        }
      } catch (error) {
        console.error("Error submitting form:", error);
      }
    };

    return { roomForm, formValid, availableAmenities, rules, submitForm, rooms };
  },
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
