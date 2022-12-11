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

	    <div class="q-pa-md row justify-center">
		<div v-for="msg in Messages" style="width: 100%; max-width: 400px">
		    <q-chat-message
			:name="msg.from_account.username"
			:avatar="msg.from_account.stripped_profile_photo"
			:text="[msg.content]"
			stamp="null minutes ago"
			       sent
			:bg-color="msg.from_account.post_color"
		    />
		</div>
	    </div>
	    
	</div>
  </q-layout>
</template>

<script>
 import { defineComponent, ref } from 'vue'
 import { useAuthStore } from '../stores/auth';
 import  NewHeader from '../components/NewHeader.vue';
 
 export default defineComponent({
     name: 'MessagingLayout',
     
     components: { NewHeader },
     data: () => {
	 return {
	     
	     Mesages: {},
	 }
     },
     async created () {
	 this.Auth = useAuthStore();
	 const valid = await this.Auth.validateSession();
	 if (this.Auth.hasAccess == false) {
	     window.location.href = "/login/";
	 }

	 this.Messages = await this.getChatroomMessages(this.Auth.userId);
	 this.Feed.posts.forEach((post) => {
	     // TODO added liked here if userid in post.likes?
	     post.likes.includes(this.Auth.userId) ? post.liked = "Liked" : post.liked = "Like"  
	     post.showComments = false;
	 })
     },
     
     methods: {
	 getChatroomMessages: async function (key) {
	     const url = "/api/chatroom/" + key + "/"
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

	 apiSendMessage: async function (key, message) {
	     const url = "/api/chatroom/send/" + key + "/"
	     const res = await fetch(url, {
		 method: "POST",
		 headers: {
		     "Content-Type": "application/json",
		     "Auth": this.Auth.refreshToken,
		 },
		 body: JSON.stringify({
		     content: message
		 })
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
