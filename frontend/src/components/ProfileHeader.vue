<script setup>
 const props = defineProps({
     username: {
	 type: String,
	 description: "username to display",
     },
     backgroundColor: {
	 type: String,
	 description: "color to display (supply static path)",
     },
     name: {
	 type: String,
	 description: "name to display",
     },
     followColor: {
	 type: String,
	 description: "color to display favorite button",
     },
     goToFollowersPage: {
	 type: String,
	 description: "function for going to followers page",
     },
     followAccount: {
	 type: String,
	 description: "function for following person",
     },
     editProfile: {
	 type: Boolean,
	 default: false,
     },
     profilePhoto: {
	 type: String,
	 description: "url to profile photo",
     },
     canEdit: {
	 type: Boolean,
	 default: false,
     },

 });
</script>
<template>
    <div class="account-header" :style="{'background-color': backgroundColor}" >
	<h3>{{username}}</h3>
	<img class="profile-photo" :src="profilePhoto">
	<h5>{{name}}</h5>
	<q-btn-group push>
	    <q-btn push color="secondary" :text-color="followColor" label="Follow" icon="favorite" />
	    <q-btn push color="secondary" @click="goToFollowersPage" label="Followers" icon="history" />
	    <q-btn push v-if="canEdit" @click="editProfile = !editProfile" color="secondary" label="Edit" icon="update" />
	</q-btn-group>
	<q-btn icon="navigation" flat  @click="followAccount" />
    </div>
</template>
<style>
 .account-header {
     width: 100%;
     display:flex;
     align-items:center;
     flex-direction:column;
 }
 
</style>
