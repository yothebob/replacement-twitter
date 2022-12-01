<template >
    <q-layout class="flex flex-center custom-background" view="lHh Lpr lFf" v-bind:style="{ backgroundImage: 'url(' + Profile.stripped_background_photo + ')' }">
      <div style="display:flex;align-items:center;flex-direction:column;">
	  <q-btn color="primary" label="Logout" @click="logoutUser" />
	  <div class="account-header" :style="{'background-color': this.Profile.post_color}" style="width: 100%;display:flex;align-items:center;flex-direction:column;" >
		  <h3>{{Profile.username}}</h3>
		  <img class="profile-photo" :src="Profile.stripped_profile_photo">
	      <h5>{{Profile.name}}</h5>
	      <q-btn-group push>
		  <q-btn push color="secondary" :text-color="[followed ? likedColor : unlikedColor]" label="Follow" icon="favorite" />
		  <q-btn push color="secondary" @click="" label="Followers" icon="history" />
		  <q-btn push v-if="Auth.userId === Profile.id" @click="editProfile = !editProfile" color="secondary" label="Edit" icon="update" />
	      </q-btn-group>
	      <q-btn icon="navigation" flat  @click="followAccount(Profile.id)" />
	  </div>
	  <div v-if="editProfile" class="edit-profile">
	      <q-input rounded outlined v-model="Profile.username" label="Username"/>
	      <q-input rounded outlined v-model="Profile.name" label="name"/>
	      <q-select v-model="Profile.post_color" :options="colorOptions" label="Post Color" />
	      <q-btn label="update" outlined  @click="updateProfile" />
	      
	  </div>
	  <div class="q-pa-md" style="width: 100%;">
	      <q-toolbar class="bg-primary text-white shadow-2">
		  <q-toolbar-title>Followers</q-toolbar-title>
	      </q-toolbar>
	      
	      <q-list bordered>
		  <q-item v-for="follow in Profile.followers" class="q-my-sm" clickable v-ripple>
		      <q-item-section avatar>

			  <div v-if="follow.stripped_profile_photo !== ''" >
			      <q-avatar color="primary" text-color="white">
				  <img size="250px"  :src="follow.stripped_profile_photo">
			      </q-avatar>
			  </div>
			  <div v-else>
			      <q-avatar color="primary" text-color="white">
				  {{follow.username.slice(0,1)}}
			      </q-avatar>
			  </div>
		      </q-item-section>
		      
		      <q-item-section>
			  <a @click="goToAccount(follow.username)">
			      <q-item-label>{{ follow.username }}</q-item-label>
			      <q-item-label caption lines="1">{{ follow.name }}</q-item-label>
			  </a>
			  <q-icon :text-color="[followed ? likedColor : unlikedColor]" label="Follow" icon="favorite" @click="followAccount(follow.id)" />
		      </q-item-section>
		      
		  </q-item>
		  
		  <q-separator />
		  <q-item-label header>Offline</q-item-label>
		  
		  <q-item v-for="contact in offline" :key="contact.id" class="q-mb-sm" clickable v-ripple> 
		      <q-item-section avatar>
			  <q-avatar>
			      {{contact.username.slice(0)}}
			  </q-avatar>
		      </q-item-section>
		      
		      <q-item-section>
			  <q-item-label>{{ contact.name }}</q-item-label>
			  <q-item-label caption lines="1">{{ contact.email }}</q-item-label>
		      </q-item-section>
		      
		      <q-item-section side>
			  <q-icon name="chat_bubble" color="grey" />
		      </q-item-section>
		  </q-item>
	      </q-list>
	  </div>
      </div>
  </q-layout>
</template>

<script>
 import { defineComponent, ref } from 'vue'
 import { useQuasar } from 'quasar'
 import { useAuthStore } from '../stores/auth';
 
 export default defineComponent({
     name: 'AccountLayout',
     components: {},
     setup () {
	 const $q = useQuasar()
	 $q.dark.set(true)
     },
     data: () => {
	 return {
	     unlikedColor: "grey",
	     Q: null,
	     darkMode: false,
	     likedColor: "red",
	     Profile: {},
	     offline: {},
	     Auth: null,
	     followed: false,
	     editProfile: false,
	     colorOptions: [],
	 }
     },

     async created () {
	 this.colorOptions = [
	     "white",
	     "red",
	     "blue",
	     "green",
	     "purple",
	     "pink",
	 ];
	 this.Auth = useAuthStore();
	 const valid = await this.Auth.validateSession();
	 if (this.Auth.hasAccess == false) {
	     window.location.href = "/login/";
	 }
	 this.Profile = await this.getProfileFollowing(this.$route.params.username);
	 this.Auth.following.includes(this.Profile.id) ? this.followed = true : this.followed = false;
     },
     methods: {
	 goToAccount: function (key) {
	     window.location.href = "/account/" + key 
	 },
	 logoutUser: function () {
	     this.Auth.clearUserSession();
	 },

	 updateProfile: async function () {
	     const url = "/api/update/"
	     const res = await fetch(url, {
		 method: "POST",
		 headers: { "Content-Type": "application/json",
			    "Auth": this.Auth.refreshToken
		 },
		 body: JSON.stringify({
		     username: this.Profile.username,
		     name: this.Profile.name,
		     post_color: this.Profile.post_color
		 })
	     })
	 },

	 followAccount: async function (followId) {
	     const url = "/api/follow/";
	     const res = await fetch (url, {
		 method: "POST",
		 headers: { "Content-Type": "application/json" },
		 body: JSON.stringify({
		     accountId: this.Auth.userId,
		     followAccountId: followId, // todo switch some of these wuth auth
		 })
	     })
	     const json = await res.json();
	     if ("success" in json) {
		 /* this.followed ? this.followed = false : this.followed = true; */
		 this.followed != this.followed
	     }
	 },

	 getProfileFollowing: async function (key) {
	     const url = "/api/account/following/" + key + "/"
	     const res = await fetch(url, {
		 method: "GET",
		 headers: { "Content-Type": "application/json" }
	     })
	     const json = await res.json();
	     return json;
	 },
	 
     },
     
 })
</script>
<style>
 .chat-message {
     max-width: 75%;
     color: white;
     word-wrap: break-word;
     border-radius: 20px;
     display: flex;
     flex-direction: column;
     align-items: center;
     justify-content: space-around;
 }
 .profile-photo {
     max-width: 400px;
     height: 300px;
     border-radius: 50%;
 }
 .custom-background {
     
 }
</style>
