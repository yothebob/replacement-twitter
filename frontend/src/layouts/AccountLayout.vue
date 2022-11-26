<template>
    <q-layout class="flex flex-center" view="lHh Lpr lFf">
      <div style="display:flex;align-items:center;flex-direction:column;">
	  <div class="account-header" style="background-color: yellow; width: 100%;display:flex;align-items:center;flex-direction:column;" >
		  <h3>{{Profile.username}}</h3>
	      <q-avatar>
		  <img size="250px" src="https://cdn.quasar.dev/img/avatar.png">
	      </q-avatar>
	      <h5>{{Profile.name}}</h5>
	      <q-btn icon="navigation" flat :text-color="[followed ? likedColor : unlikedColor]" @click="followAccount" />
	  </div>
	  <div class="create-post">
		  <q-btn label="Create Post" flat  @click="showCreatePost = !showCreatePost" />
		  <div v-if="showCreatePost" class="create-post-form">
		      <q-input filled v-model="newPostTitle" label="Filled" /><br/>
		      <q-input filled v-model="newPostContent" type="textarea" /><br/>
		      <q-input
			  @update:model-value="val => { file = val[0] }"
			  filled
			  type="file"
			  hint="Native file"
		      />
		  </div>
	  </div>
	  <div v-for="post in Profile.posts">
	      <div class="q-pa-md row items-start q-gutter-md" >
		  <q-card class="my-card" :color="post.account_post_color" style="width: 450px;" >
		       <q-card-section>
			   <div class="text-h6">{{post.title}}</div>
			   <div class="text-subtitle2">by {{Profile.username}}</div>
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
 import { useQuasar } from 'quasar'
 
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
	     likedColor: "red",
	     Profile: {},
	     darkMode: false,
	     followed: false,
	     showCreatePost: false,
	 }
     },

     async created () {
	 this.Profile = await this.getProfilePosts(1);
	 this.Profile.posts.forEach((post) => {
	     // TODO added liked here if userid in post.likes?
	     
	     post.likes.includes(this.Profile.id) ? post.liked = this.likedColor : post.liked = this.unlikedColor
	     post.showComments = false;
	 })
	 //                         fix with authjs \/
	 this.Profile.following.includes(this.Profile.id) ? this.followed = true : this.followed = false;
     },
     
     methods: {
	 followAccount: async function () {
	     const url = "/api/follow/";
	     const res = await fetch (url, {
		 method: "POST",
		 headers: { "Content-Type": "application/json" },
		 body: JSON.stringify({
		     accountId: this.Profile.id,
		     followAccountId: 2, // todo switch some of these wuth auth
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
