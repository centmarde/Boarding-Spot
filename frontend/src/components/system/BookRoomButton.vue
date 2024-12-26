<!-- BookRoomButton.vue -->
<template>
    <v-btn color="primary" @click="handleClick">Book This Room</v-btn>
  </template>
  
  <script setup lang="ts">
  import { supabase } from '@/lib/supabase';
  import { useToast } from 'vue-toastification';

  const toast = useToast();

  const handleClick = async () => {
    const confirmed = confirm('Are you sure you want to book this room?');
    if (!confirmed) return; // Exit if the user cancels

    console.log('Booking room...');
    const { data, error } = await supabase
      .from('rooms')
      .insert([
        { add: true },
      ])
      .select();

    if (error) {
        console.error('Error inserting room:', error);
    } else {
       toast.success('Room booked successfully');
    }
  };
  </script>
  
  <style scoped>
  /* Add any specific styles for the button here */
  </style>
  