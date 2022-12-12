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
		<div style="width: 100%; max-width: 400px">
		    <div v-for="msg in Messages.chatroom_messages" >
			<q-chat-message
			    v-if="msg.from_account.id == this.Auth.userData.id"
			    :name="msg.from_account.username"
			    :avatar="msg.from_account.stripped_profile_photo ? msg.from_account.stripped_profile_photo : undefined"
			    :text="[msg.content]"
			    stamp="null minutes ago"
			    sent
			    :bg-color="msg.from_account.post_color"
			/>
			<q-chat-message
			    v-else
			    :name="msg.from_account.username"
			    :avatar="msg.from_account.stripped_profile_photo ? msg.from_account.stripped_profile_photo : undefined"
			    :text="[msg.content]"
			    stamp="null minutes ago"
			    :bg-color="msg.from_account.post_color"
			/>
		    </div>		
		</div>	
	    </div>
	    <div class="message-input-bar">
	    <q-input rounded outlined v-model="typedMessage" label="" >
		<template v-slot:after>
		    <q-btn round dense flat
			   icon="send"
			   @click="apiSendMessage"
			   error-message="Something went wrong..."
			   :error="sendError"
		    />
		</template>
	    </q-input>
	    </div>
	    <div class="input-invisible-pad"></div>
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
	     
	     Messages: {},
	     typedMessage: "",
	     sendError: false,
	     errorMessage: null,
	     timer: null,
	 }
     },
     async created () {
	 this.Auth = useAuthStore();
	 const valid = await this.Auth.validateSession();
	 if (this.Auth.hasAccess == false) {
	     window.location.href = "/login/";
	 }

	 this.Messages = await this.getChatroomMessages(this.$route.params.chatroom);
     },
     mounted: function () {
	 this.timer = setInterval(() => {
	     this.apiCheckMessages(this.$route.params.chatroom);
	 }, 5000);
     },
     beforeDestroy() {
	 clearInterval(this.timer)
     },
     methods: {
	 apiCheckMessages: async function (key) {
	     const url = "/api/chatroom/check/" + key + "/"
	     const res = await fetch(url, {
		 method: "GET",
		 headers: {
		     "Content-Type": "application/json",
		     "Auth": this.Auth.refreshToken,
		     "lastKey": this.Messages.chatroom_messages[this.Messages.chatroom_messages.length -1 ].id,
		 }
	     })
	     const json = await res.json();
	     if ("success" in json) {
		 this.Messages.chatroom_messages = [...this.Messages.chatroom_messages, ...json.updated];
	     }
	     
	 },
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

	 apiSendMessage: async function () {
	     const url = "/api/chatroom/send/" + this.$route.params.chatroom + "/"
	     const res = await fetch(url, {
		 method: "POST",
		 headers: {
		     "Content-Type": "application/json",
		     "Auth": this.Auth.refreshToken,
		 },
		 body: JSON.stringify({
		     content: this.typedMessage
		 })
	     })
	     const json = await res.json();
	     if ( "success" in json ) {
		 this.sendError = false;
		 this.Messages = {...json.updated}
	     } else {
		 this.sendError = true;
		 this.errorMessage = json.error;
	     }
	     this.typedMessage = "";
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
<style>

 .message-input-bar {
     width: 90%;
     background-color: white;
     position: fixed;
     bottom: 2%;
 }
 .input-invisible-pad {
     margin-top: 4rem;
 }
</style>
