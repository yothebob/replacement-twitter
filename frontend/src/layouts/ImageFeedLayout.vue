<template>
    <q-layout class="flex flex-center custom-background" view="lHh Lpr lFf" v-bind:style="{ backgroundImage: 'url(' + Auth.userData.stripped_background_photo + ')' }">
	<div style="display:flex;align-items:center;flex-direction:column;">
	    <NewHeader
		:backgroundColor="Auth.userData.post_color"
		:logout="logoutuser"
		:dark="Auth.setDarkMode"
		:profileLink="`/account/${Auth.userData.username}`"
		feedLink="/feed"
		imageLink="/images"
		chatLink="/chatrooms"
	    ></NewHeader>
	    <div style="display:flex;justify-content:space-around;"><h3>{{Auth.userData.username}}'s Feed</h3></div>
	    <div v-for="post in Feed.posts">
	      <div class="q-pa-md row items-start q-gutter-md" >
		  <q-card class="my-card" :style="{'color' : post.post_creator_post_color}" style="width: 450px;" >
		       <q-card-section>
			   <div class="text-h6">{{post.title}}</div>
			   <div class="text-subtitle2">by {{post.post_creator_username}}</div>
		       </q-card-section>

			   
		       <q-card-section v-if="post.stripped_image != 'None' || post.stripped_image != ''">
		           <q-img :src="post.stripped_image"></q-img>
		       </q-card-section>

		       
		       <q-card-section>
			   {{ post.content }}
		       </q-card-section>
		       
		       <q-separator dark />
		       
		       <q-card-actions>
			   <q-btn @click="likeItem(Auth.userId, post.id,'post',post)" :text-color="post.liked" icon="favorite"> {{post.likes.length}}</q-btn>
			   <q-btn @click="postShowComments(post)" flat> Comments {{post.comments.length}}</q-btn>
		       </q-card-actions>

		       <div v-if="post.showComments" >
			   <div v-for="comment in post.comments">
			       <q-card-section>
				   <div class="chat-message" :style="{'background-color': comment.account_comment_color}">
				       <p><strong>{{comment.account_username}}</strong>
					   <q-avatar>
					       <img size="250px" style="padding:5px; margin:5px;" :src="Auth.userData.stripped_profile_photo">
					   </q-avatar>

				       </p>
				       <p>
					   {{ comment.body }}
				       </p>
				       <q-btn flat icon="favorite" style="width:50px;" :text-color="comment.liked" @click="likeItem(Auth.userId, comment.id,'comment',comment)"> {{comment.likes.length}} </q-btn>
				   </div>
			       </q-card-section>
			       
			       <q-separator dark />
			       
			   </div>
			   <q-input outlined v-model="newComment" :dense="dense">
			       <template v-slot:append>
				   <q-avatar>
				       <q-icon name="send" @click="submitComment(Auth.userId,post)" class="cursor-pointer" />
				   </q-avatar>
			       </template>
			   </q-input>
		       </div>
		  </q-card>
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
