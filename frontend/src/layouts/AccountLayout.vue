<template >
    <q-layout class="flex flex-center custom-background" view="lHh Lpr lFf" v-bind:style="{ backgroundImage: 'url(' + Profile.stripped_background_photo + ')' }">
      <div style="display:flex;align-items:center;flex-direction:column;">
	  <div class="account-header" :style="{'background-color': this.Profile.post_color}" style="width: 100%;display:flex;align-items:center;flex-direction:column;" >
		  <h3>{{Profile.username}}</h3>
		  <img class="profile-photo" :src="Profile.stripped_profile_photo">
	      <h5>{{Profile.name}}</h5>
	      <q-btn icon="navigation" flat :text-color="[followed ? likedColor : unlikedColor]" @click="followAccount" />
	  </div>
	  <div class="create-post">
		  <q-btn label="Create Post" flat  @click="showCreatePost = !showCreatePost" />
		  <div v-if="showCreatePost" class="create-post-form">
		      <q-input filled v-model="newPostTitle" label="Title" /><br/>
		      <q-input filled v-model="newPostContent" type="textarea" /><br/>
		      <q-input
			  @update:model-value="val => { file = val[0] }"
			  filled
			  type="file"
			  hint="Native file"
		      />
		      <q-btn label="Post" outlined  @click="CreateNewPost" />
		  </div>
	  </div>
	  <div v-for="post in Profile.posts">
	      <div class="q-pa-md row items-start q-gutter-md" >
		  <q-card class="my-card" :style="{'color' : post.post_creator_post_color}" style="width: 450px;" >
		       <q-card-section>
			   <div class="text-h6">{{post.title}}</div>
			   <div class="text-subtitle2">by {{post.post_creator_username}}</div>
		       </q-card-section>

			   
		       <q-card-section v-if="post.stripped_image">
		           <q-img :src="post.stripped_image"></q-img>
		       </q-card-section>

		       <q-card-section v-if="post.stripped_video">
			   <q-video :src="post.stripped_video" />
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
					       <img size="250px" style="padding:5px; margin:5px;" :src="Profile.stripped_profile_photo">
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
	     newComment: '',
	     unlikedColor: "grey",
	     Q: null,
	     darkMode: false,
	     likedColor: "red",
	     Profile: {},
	     Auth: null,
	     darkMode: false,
	     followed: false,
	     showCreatePost: false,
	     newPostTitle: "",
	     newPostContent: "",

	 }
     },

     async created () {
	 console.log( this.$route.params.username)
	 this.Auth = useAuthStore();
	 const valid = await this.Auth.validateSession();
	 if (this.Auth.hasAccess == false) {
	     window.location.href = "/login/";
	 }
	 this.Profile = await this.getProfilePosts(this.$route.params.username);
	 this.Profile.posts.forEach((post) => {
	     // TODO added liked here if userid in post.likes?
	     
	     post.likes.includes(this.Auth.userId) ? post.liked = this.likedColor : post.liked = this.unlikedColor
	     post.showComments = false;
	 })
	 this.Auth.following.includes(this.Profile.id) ? this.followed = true : this.followed = false;
     },
     methods: {
	 CreateNewPost: async function () {
	     const url = "/api/post/";
	     let image = "";
	     let video = "";
	     const res = await fetch(url, {
		 method: "POST",
		 headers: { "Content-Type": "application/json" },
		 body: JSON.stringify({
		     account: this.Profile.id,
		     postCreator: this.Auth.userId,
		     title: this.newPostTitle,
		     content: this.newPostContent,
		     image: "",
		     video: "",
		 })
	     })
	     const json = await res.json();
	     this.showCreatePost = false;
	     if ("success" in json) {
		 this.Profile.posts.push(json.post)
	     }
	 }, 
	 followAccount: async function () {
	     const url = "/api/follow/";
	     const res = await fetch (url, {
		 method: "POST",
		 headers: { "Content-Type": "application/json" },
		 body: JSON.stringify({
		     accountId: this.Auth.userId,
		     followAccountId: this.Profile.id, // todo switch some of these wuth auth
		 })
	     })
	     const json = await res.json();
	     if ("success" in json) {
		 this.followed ? this.followed = false : this.followed = true;
		 this.followed != this.followed
	     }
	 },

	 submitComment: async function(accountId, post) {
	     const url = "/api/comment/"
	     const res = await fetch(url, {
		 method: "POST",
		 headers: { "Content-Type": "application/json" },
		 body: JSON.stringify({
		     accountId: accountId,
		     body: this.newComment,
		     postId: post.id
		 })
	     })
	     this.newComment = "";
	     const json = await res.json();
	     if ( "success" in json) {
		 console.log(json.newComment)
		 post.comments.push(json.newComment)
	     }
	 },

	 getProfilePosts: async function (key) {
	     const url = "/api/Account/" + key + "/"
	     const res = await fetch(url, {
		 method: "GET",
		 headers: { "Content-Type": "application/json" }
	     })
	     const json = await res.json();
	     return json;
	 },

	 postShowComments: function (post) {
	     post.showComments = !post.showComments
	     post.comments.forEach((comment) => {
		 comment.liked = "white";
		 comment.likes.includes(this.Auth.userId) ? comment.liked = this.likedColor : comment.liked = this.unlikedColor;
	     }) 
	 },
	 
	 likeItem: async function (accountKey, itemKey, item, itemObj) {
	     if (itemObj.liked ===  this.likedColor) {
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
		 itemObj.liked = this.likedColor
		 itemObj.likes.push(accountKey)
	     } 
	 }
	 
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
