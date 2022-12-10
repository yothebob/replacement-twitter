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
	    </div>
	    <div v-if="Profile.chatRooms">
		<q-list bordered>
		<div v-for="room in Profile.chatRooms">
		    <q-item @click="enterChatRoom(room)" clickable v-ripple>

			<q-item-section>
			    <q-item-label>{{room.name}}</q-item-label>
			    <q-item-label caption lines="2">
				{{room.messageList[-1].content}}
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
 
 export default defineComponent({
     name: 'FeedLayout',
     
     components: { NewHeader },
     data: () => {
	 return {
	     
	     Feed: {},
	 }
     },
     async created () {
	 this.Auth = useAuthStore();
	 this.Feed = await this.getProfileFeed(this.Auth.userId);
	 this.Feed.posts.forEach((post) => {
	     // TODO added liked here if userid in post.likes?
	     post.likes.includes(this.Auth.userId) ? post.liked = "Liked" : post.liked = "Like"  
	     post.showComments = false;
	 })
     },
     
     methods: {
	 getProfileFeed: async function (key) {
	     const url = "/api/account/feed/" + key + "/"
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

	 likeItem: async function (accountKey, itemKey, item, itemObj) {
	     if (itemObj.liked ===  "Liked") {
		 return;
	     }
	     const url = "/api/like/";
	     const res = await fetch(url, {
		 method: "POST",
		 headers: { "Content-Type": "application/json" },
		 body: JSON.stringify({
		     accountKey: accountKey,
		     itemKey: itemKey,
		     item: item,
		 })
	     })
	     const json = await res.json();
	     if ("success" in json) {
		 itemObj.liked = "Liked"
		 itemObj.likes.push(accountKey)
	     } 
	 }
	 
     },
     
 })
</script>
