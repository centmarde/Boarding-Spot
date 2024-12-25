<template>
    <v-card class="py-5 bg-card">
        <v-container>
    <v-form ref="form" v-model="formValid">
        <v-text-field
            v-model="roomForm.title"
            :rules="[rules.required, rules.maxLength(50)]"
            label="Title"
            required
          
          ></v-text-field>
      <v-row>
       
       
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
      <v-btn style="width: 100%;" :disabled="!formValid" color="primary" @click="submitForm"
        >Submit</v-btn
      >
    </v-form>
  </v-container>
    </v-card>
  
</template>

<script>
import { ref } from "vue";
import { useRoomStore } from "@/stores/roomStore";

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
    });

    const formValid = ref(false);

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
        await createRoom(roomForm.value);
        alert("Room created successfully!");
      } catch (error) {
        console.error("Error submitting form:", error);
      }
    };

    return { roomForm, formValid, availableAmenities, rules, submitForm };
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
