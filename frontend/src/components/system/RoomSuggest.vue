<template>
    <v-container>
        <v-row align="center" justify="center">
            <v-col cols="8" sm="8" md="8">
                <div class="input-wrapper">
                    <input type="text" placeholder="Type here..." name="text" class="input">
                </div>
            </v-col>
            <v-col cols="12" sm="4" md="2">
                <v-btn color="#00b7ff" @click="generateSuggestion" block>
                    Find Room
                </v-btn>
            </v-col>
        </v-row>
        <br> 
    </v-container>
</template>

<script lang="ts" setup>
import { ref } from 'vue';

const suggestion = ref('');

function generateSuggestion() {
    // Logic to generate a suggestion
    suggestion.value = 'Sample Room Suggestion';
}
</script>

<style scoped>
.input-wrapper input {
    background-color: #eee;
    border: 2px solid #00b7ff;
    padding: 1rem;
    font-size: 1rem;
    width: 45em;
    border-radius: 1rem;
    color: #00b7ff;
    box-shadow: 0 0.4rem #dfd9d9;
    cursor: pointer;
}

.input-wrapper input:focus {
    outline-color: #00b7ff;
}

@media (max-width: 768px) {
    .input-wrapper input {
        width: 14em;
    }
}
</style>
