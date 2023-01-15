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
		    <div v-for="msg in Messages.chatroom_messages" id="chat-div">
			<div v-if="msg.stripped_image != ''" style="padding: 20px;">
			    <q-img
				:src="msg.stripped_image"
				spinner-color="white"
				style="height: 200px; max-width: 200px"
			    />
			</div>
			<div v-else-if="msg.stripped_video != ''" style="padding: 20px;">
			    <video-player
				:src="msg.stripped_video"
				controls
				width="320"
				height="240"
			    />
			</div>
			<div v-if="msg.content != ''">
			    <q-chat-message
				v-if="msg.from_account.id == this.Auth.userData.id"
				:name="msg.from_account.username"
				:avatar="msg.from_account.stripped_profile_photo ? msg.from_account.stripped_profile_photo : undefined"
				:text="[msg.content]"
				:stamp="msg.timeCreated"
				sent
				:bg-color="msg.from_account.post_color"
			    />
			    <q-chat-message
				v-else
				:name="msg.from_account.username"
				:avatar="msg.from_account.stripped_profile_photo ? msg.from_account.stripped_profile_photo : undefined"
				:text="[msg.content]"
				:stamp="msg.timeCreated"
				:bg-color="msg.from_account.post_color"
			    />
			</div>
		    </div>		
		</div>	
	    </div>
	    <div class="message-input-bar">
		<div >
		<q-file  style="width:50px;font-size:0;" v-model="msgUploadedImage">
		    <template v-slot:prepend>
			<q-icon name="attach_file" />
		    </template>
		</q-file>
		</div>
		<div style="width:95%;">
	  	<q-input rounded outlined
			 v-model="typedMessage"
			 label=""
			 v-on:keyup.enter="apiSendMessage"
		>
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
	    </div>
	    <div class="input-invisible-pad" id="msg-div"></div>
	</div>
  </q-layout>
</template>

<script>
 import { defineComponent, ref } from 'vue'
 import { useAuthStore } from '../stores/auth';
 import  NewHeader from '../components/NewHeader.vue';
 import emojis from '../emoji.js';
 import { VideoPlayer } from '@videojs-player/vue'
 import 'video.js/dist/video-js.css'
 
 export default defineComponent({
     name: 'MessagingLayout',
     
     components: { NewHeader, VideoPlayer },
     data: () => {
	 return {
	     search: '',
	     Messages: {},
	     msgUploadedImage: null,
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
	 this.Messages.chatroom_messages = this.Messages.chatroom_messages.reverse();

	 for (const [key, val] of Object.entries( emojis.emojis.Objects)) {
	     console.log(val)
	 }
	 /* this.typedMessage */
     },
     mounted: function () {
	 this.timer = setInterval(() => {
	     this.apiCheckMessages(this.$route.params.chatroom);
	 }, 5000);
     },
     beforeDestroy() {
	 clearInterval(this.timer);
     },
     methods: {
	 insert: function (emoji) {
	     this.typedMessage += emoji;
	 },
	 addMessageImage: async function (msgId) {
	     var data = new FormData()
	     data.append('image', this.msgUploadedImage)
	     const videos = [".mp4", ".mov", ".wmv", ".mkv", ".webm", ".m4a", ".m4v",".avi", ".ogg" ,".mpg", ".mpeg", ".flv"]
	     let is_image = "True"
	     let ext_type = ""
	     videos.forEach((it) => {
		 if (this.msgUploadedImage.name.includes(it)) {
		     is_image = "False"
		     ext_type = it
		 }
	     });
	 const imageAdd = await fetch("/api/image/add/",{
		     method: "POST",
		 headers: { "Auth": this.Auth.refreshToken,
			    "type": "message",
			    "id": msgId ,
			    "image": is_image,
			    "ext": ext_type
		 }, 
		 body: data,
	     })
	     const j = await imageAdd.json();
	     if (is_image) {
		 return j.stripped_image;
	     } else {
		 return j.stripped_video;
	     }
	 },
	 
	 notify: function (message) {
	     if (!("Notification" in window)) {
		 alert("This browser does not support desktop notification");
	     } else if (Notification.permission === "granted") {
		 const notification = new Notification(message);
	     } else if (Notification.permission !== "denied") {
		 Notification.requestPermission().then((permission) => {
		     if (permission === "granted") {
			 const notification = new Notification(message);
		     }
		 });
	     }
	 },
	 
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
		 if (json.updated.length > 0) {
		     this.notify("New Message")
		 }
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
		 if (this.msgUploadedImage != null){
		     const sentImage = await this.addMessageImage(json.newMsg.id);
		     json.newMsg.stripped_image = sentImage
		     this.msgUploadedImage = null;
		     this.Messages.chatroom_messages.push(json.newMsg)
		 } else {
		     this.Messages.chatroom_messages.push(json.newMsg)
		 }
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
     display: flex;
     flex-direction: row;
     width: 100%;
     background-color: white;
     position: fixed;
     bottom: 2%;
 }
 .input-invisible-pad {
     margin-top: 4rem;
 }
</style>
