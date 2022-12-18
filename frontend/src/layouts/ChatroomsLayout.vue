<template>
    <q-layout class="flex flex-center custom-background" view="lHh Lpr lFf" v-bind:style="{ backgroundImage: 'url(' + Auth.userData.stripped_background_photo + ')' }">
	<div style="display:flex;align-items:center;flex-direction:column;">
	    <NewHeader
		:backgroundColor="Auth.userData.post_color"
		:logout="Auth.clearUserSession"
		:dark="Auth.setDarkMode"
		:profileLink="`/account/${Auth.userData.username}`"
		feedLink="/feed"
		imageLink="/images"
		chatLink="/chatrooms"
	    ></NewHeader>

	    <div style="display:flex;justify-content:space-around;"><h3>Chat Rooms</h3></div>
	    <div>
		<q-btn label="Create New Chatroom" @click="" />
		<div>
		    
		    
		</div>
	    </div>
	    <div style="margin:2rem;"></div>
	    <div v-if="chatRooms">
		<q-list bordered>
		<div v-for="room in chatRooms">
		    <q-item @click="router.push({'path': '/message/' + room.btoaName})" clickable v-ripple>

			<q-item-section>
			    <q-item-label>{{room.name}}</q-item-label>
			    <q-item-label caption lines="1">
				{{room.chatroom_messages[room.chatroom_messages.length -1 ].content}}
			    </q-item-label>
			</q-item-section>
			
			<q-item-section></q-item-section>

			<q-item-section avatar>
			    <div v-if="room.stripped_profile_photo" >
				<q-avatar color="primary" text-color="white">
				    <img size="250px"  :src="room.stripped_profile_photo">
				</q-avatar>
			    </div>
			    <div v-else>
				<q-avatar color="primary" text-color="white">
				    {{room.name.slice(0,1)}}
				</q-avatar>
			    </div>
			</q-item-section>
		    </q-item>
		    <q-separator />
		</div>
		
		</q-list>
	    </div>
	    <div v-else>
		<h3>You have No room, create one!</h3>
	    </div>
      </div>
  </q-layout>
</template>

<script>
 import { defineComponent, ref } from 'vue'
 import { useAuthStore } from '../stores/auth';
 import  NewHeader from '../components/NewHeader.vue';
 import { useRouter } from 'vue-router';
 
 export default defineComponent({
     name: 'ChatroomsLayout',
     
     components: { NewHeader },
     data: () => {
	 return {
	     chatRooms: {},
	     accounts: [],
	     newName: null,
	     newAccounts: null,
	     create: false,
	     router: null,
	 }
     },
     async created () {
	 this.router = useRouter();
	 this.Auth = useAuthStore();
	 /* const all_accounts = await this.allAccounts();
	    Array.from(all_accounts).forEach((act) => { this.accounts.push(act.username) }) */
	 const valid = await this.Auth.validateSession();
	 if (this.Auth.hasAccess == false) {
	     window.location.href = "/login/";
	 }

	 this.chatRooms = await this.getChatRooms(this.Auth.userId);
	 Array.from(this.chatRooms).forEach((cr) => {
	     cr.chatroom_messages.reverse();
	 })
	 this.chatRooms.forEach((cr) => {
	     cr.btoaName = btoa(`${cr.name}|||${cr.id}`);
	 })
     },
     
     methods: {
	 getChatRooms: async function (key) {
	     const url = "/api/chatrooms" + "/"
	     const res = await fetch(url, {
		 method: "GET",
		 headers: {
		     "Content-Type": "application/json",
		     "Auth": this.Auth.refreshToken,
		 }
	     })
	     const json = await res.json();
	     return json;
	 },
     },
     
 })
</script>
