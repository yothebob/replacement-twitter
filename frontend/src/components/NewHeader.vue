<script setup>
 import { useRouter } from 'vue-router';
 import { ref } from 'vue';
 const router = useRouter();
 const props = defineProps({
     backgroundColor: {
	 type: String,
	 description: "color to display (supply static path)"
     },
     logout: {
	 type: String,
	 description: "Field Label"
     },
     dark: {
	 type: String,
	 description: "Value to display"
     },
     profileLink: {
	 type: String,
	 default: "/account",
	 description: "Value to display"
     },
     feedLink: {
	 type: String,
	 default: "/feed",
	 description: "feed link",
     },
     imageLink: {
	 type: String,
	 default: "/images",
	 description: "image link"
     }
 });
</script>
<template>
    <q-header elevated :style="{'background-color': backgroundColor}">
        <q-toolbar>
	    <div class="row justify-start">
		<q-btn label="Logout" @click="logout" />
		<q-btn label="dark mode" @click="dark" />
		<q-btn name="Feed" label="Feed" @click="router.push({path : feedLink })" />
		<q-btn name="Profile" label="Profile" @click="router.push({path : profileLink })" />
		<q-btn name="Images" label="Images" @click="router.push({path : imageLink})" />
	    </div>
	</q-toolbar>
    </q-header>
</template>

