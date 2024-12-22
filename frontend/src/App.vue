<template>
  <v-app>
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script lang="ts" setup>
import { useTheme } from 'vuetify';

const theme = useTheme();

function toggleTheme() {
  theme.global.name.value = theme.global.current.value.dark ? 'light' : 'dark';
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Mea+Culpa&display=swap');

.v-main {
  overflow-x: hidden; /* Prevent horizontal overflow */
}
</style>
