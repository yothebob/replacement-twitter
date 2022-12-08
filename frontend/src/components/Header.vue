<script setup>
 const props = defineProps({
     logout: {
	 type: String,
	 description: "Field Label",
     },
     dark: {
	 type: String,
	 description: "Value to display",
     },
 });
</script>
<template>
    <q-btn color="primary" label="Logout" @click="logout" />
    <q-btn color="secondary" label="dark mode" @click="dark" />
</template>

