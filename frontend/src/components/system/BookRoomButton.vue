<!-- BookRoomButton.vue -->
<template>
    <v-btn color="primary" @click="handleClick">Book this room</v-btn>
  </template>
  
  <script setup lang="ts">
  import { defineEmits } from 'vue';
  
  // Emit the event when the button is clicked
  const emit = defineEmits();
  
  const handleClick = () => {
    // Emit a custom event when the button is clicked
    emit('book-room');
  };
  </script>
  
  <style scoped>
  /* Add any specific styles for the button here */
  </style>
  