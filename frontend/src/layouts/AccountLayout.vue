<template>
    <q-layout class="flex flex-center" view="lHh Lpr lFf">
      <div>
	  <h3>{{Profile.username}}</h3>
	  <h5>{{Profile.name}}</h5>
	  <div v-for="post in Profile.posts">
	      <div class="q-pa-md row items-start q-gutter-md" >
		  <q-card class="my-card" :color="post.account_post_color" style="width: 500px;" >
		       <q-card-section>
			   <div class="text-h6">{{post.title}}</div>
			   <div class="text-subtitle2">by {{Profile.username}}</div>
		       </q-card-section>

			   
		       <q-card-section v-if="post.image">
		           <q-img src="https://cdn.quasar.dev/img/parallax2.jpg"></q-img>
		       </q-card-section>

		       <q-card-section v-if="post.video">
			   <q-video src="https://www.youtube.com/embed/k3_tw44QsZQ?rel=0" />
		       </q-card-section>

		       
		       <q-card-section>
			   {{ post.content }}
		       </q-card-section>
		       
		       <q-separator dark />
		       
		       <q-card-actions>
			   <q-btn @click="likeItem(Profile.id, post.id,'post',post)" :text-color="post.liked" icon="favorite"> {{post.likes.length}}</q-btn>
			   <q-btn @click="postShowComments(post)" flat> Comments {{post.comments.length}}</q-btn>
		       </q-card-actions>

		       <div v-if="post.showComments" >
			   <div v-for="comment in post.comments">
			       <q-card-section>
				   <div class="chat-message">
				       <p><strong>{{comment.account_username}}</strong></p>
				       <p>
					   {{ comment.body }}
				       </p>
				       <q-btn flat icon="favorite" style="width:50px;" :text-color="comment.liked" @click="likeItem(Profile.id, comment.id,'comment',comment)"> {{comment.likes.length}} </q-btn>
				   </div>
			       </q-card-section>
			       
			       <q-separator dark />
			       
			   </div>
			   <q-input outlined v-model="newComment" :dense="dense">
			       <template v-slot:append>
				   <q-avatar>
				       <q-icon name="send" @click="submitComment(Profile.id,post)" class="cursor-pointer" />
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

export default defineComponent({
     name: 'AccountLayout',
     
     components: {},

     data: () => {
	 return {
	     newComment: '',
	     unlikedColor: "grey",
	     likedColor: "red",
	     Profile: {},
	 }
     },

     async created () {
	 this.Profile = await this.getProfilePosts(1);
	 this.Profile.posts.forEach((post) => {
	     // TODO added liked here if userid in post.likes?
	     post.likes.includes(this.Profile.id) ? post.liked = this.likedColor : post.liked = this.unlikedColor
	     post.showComments = false;
	 })
     },
     
     methods: {

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
		 comment.likes.includes(this.Profile.id) ? comment.liked = this.likedColor : comment.liked = this.unlikedColor;
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
     word-wrap: break-word;
     background-color: green;
     border-radius: 20px;
     display: flex;
     flex-direction: column;
     align-items: center;
     justify-content: space-around;
 }
 
</style>
