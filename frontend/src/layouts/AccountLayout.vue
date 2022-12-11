<template >
    <q-layout class="flex flex-center custom-background" view="lHh Lpr lFf" v-bind:style="{ backgroundImage: 'url(' + Profile.stripped_background_photo + ')' }">
	<div style="display:flex;align-items:center;flex-direction:column;">
	    <NewHeader
		:backgroundColor="Profile.post_color"
		:logout="logoutUser"
		:dark="Auth.setDarkMode"
		:profileLink="`/account/${Profile.username}`"
		feedLink="/feed"
		imageLink="/images"
		chatLink="/chatrooms"
	    ></NewHeader>

	    <div class="account-header" :style="{'background-color': Profile.post_color}" >
		<h3>{{Profile.username}}</h3>
		<img class="profile-photo" :src="Profile.stripped_profile_photo">
		<h5>{{Profile.name}}</h5>
		<q-btn-group push>
		    <q-btn push color="secondary" :text-color="[followed ? likedColor : unlikedColor]" label="Follow" icon="favorite" />
		    <q-btn push color="secondary" @click="goToFollowersPage" label="Followers" icon="history" />
		    <q-btn push v-if="Auth.userId === Profile.id" @click="editProfile = !editProfile" color="secondary" label="Edit" icon="update" />
		</q-btn-group>
		<q-btn icon="navigation" flat  @click="followAccount" />
	    </div>

	    <div v-if="editProfile" class="edit-profile">
	      <q-input rounded outlined v-model="Profile.username" label="Username"/>
	      <q-input rounded outlined v-model="Profile.name" label="name"/>
	      <q-select v-model="Profile.post_color" :options="colorOptions" label="Post Color" />
	      <q-btn label="Update" outlined  @click="updateProfile" />
	      <div>
		   <q-file outlined v-model="uploadedImage">
		       <template v-slot:prepend>
			   <q-icon name="attach_file" />
		       </template>
		   </q-file>
		   <q-btn label="Background Image update" outlined  @click="updateBackgroundPhoto" />
	      </div>
	      <div>
		  <q-file outlined v-model="uploadedImage">
		      <template v-slot:prepend>
			  <q-icon name="attach_file" />
		      </template>
		  </q-file>
		  <q-btn label="Profile Image update" outlined  @click="updateProfilePhoto" />

	      </div>
	  </div>
	  <div class="create-post">
		  <q-btn label="Create Post" flat  @click="showCreatePost = !showCreatePost" />
		  <div v-if="showCreatePost" class="create-post-form">
		      <q-input filled v-model="newPostTitle" label="Title" /><br/>
		      <q-input filled v-model="newPostContent" type="textarea" /><br/>
		      <q-file outlined v-model="uploadedImage">
			  <template v-slot:prepend>
			      <q-icon name="attach_file" />
			  </template>
		      </q-file>
		      <q-btn label="Post" outlined  @click="CreateNewPost" />
		  </div>
	  </div>
	  <div v-for="post in Profile.posts">
	      <div class="q-pa-md row items-start q-gutter-md" >
		  <q-card class="my-card" :style="{'color' : post.post_creator_post_color}" style="width: 450px;" >
		       <q-card-section>
			   <div class="text-h6">{{post.title}}</div>
			   <div class="text-subtitle2">by {{post.post_creator_username}}</div>
			   <div class="text-subtitle4">created {{post.timeCreated}}</div>
		       </q-card-section>

			   
		       <q-card-section v-if="post.stripped_image !== ''">
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
 import { useAuthStore } from '../stores/auth';
 import  Header from '../components/Header.vue';
 import  NewHeader from '../components/NewHeader.vue';
 import  ProfileHeader from '../components/ProfileHeader.vue';

 
 export default defineComponent({
     name: 'AccountLayout',
     components: {
	 Header,
	 NewHeader,
	 ProfileHeader
     },
     setup () {
     },
     data: () => {
	 return {
	     uploadedImage: null,
	     newComment: '',
	     unlikedColor: "grey",
	     likedColor: "red",
	     Profile: {},
	     Auth: null,
	     followed: false,
	     showCreatePost: false,
	     newPostTitle: "",
	     newPostContent: "",
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
	 this.Profile = await this.getProfilePosts(this.$route.params.username);
	 this.Profile.posts.forEach((post) => {
	     // TODO added liked here if userid in post.likes?
	     
	     post.likes.includes(this.Auth.userId) ? post.liked = this.likedColor : post.liked = this.unlikedColor
	     post.showComments = false;
	 })
	 this.Auth.following.includes(this.Profile.id) ? this.followed = true : this.followed = false;
     },
     methods: {
	 goToFollowersPage: function() {
	     window.location.href = "/followers/" + this.Profile.username 
	 },
	 logoutUser: function () {
	     this.Auth.clearUserSession();
	 },
	 updateProfile: async function () {
	     console.log("work")
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

	 updateProfilePhoto: async function () {
	     var data = new FormData()
	     data.append('image', this.uploadedImage)
	     const res = await fetch("/api/image/add/",{
		 method: "POST",
		 headers: { "Auth": this.Auth.refreshToken,
			    "type": "profile",
			    "id": this.Auth.userId 
		 }, 
		 body: data,
	     })
	     const j = await imageAdd.json()
	     this.Profile.stripped_profile_photo = j.stripped_image
	 },

	 updateBackgroundPhoto: async function () {
	     var data = new FormData()
	     data.append('image', this.uploadedImage)
	     const res = await fetch("/api/image/add/",{
		 method: "POST",
		 headers: { "Auth": this.Auth.refreshToken,
			    "type": "background",
			    "id": this.Auth.userId 
		 }, 
		 body: data,
	     })
	     const j = await imageAdd.json()
	     this.Profile.stripped_background_photo = j.stripped_image
	 },
	 
	 CreateNewPost: async function () {
	     const url = "/api/post/";
	     
	     const res = await fetch(url, {
		 method: "POST",
		 headers: { "Content-Type": "application/json" }, 
		 body: JSON.stringify({
		     account: this.Profile.id,
		     postCreator: this.Auth.userId,
		     title: this.newPostTitle,
		     content: this.newPostContent,
		 })
	     })
	     const json = await res.json();
	     this.showCreatePost = false;
	     if ("success" in json) {
		 var data = new FormData()
		 data.append('image', this.uploadedImage)
		 const imageAdd = await fetch("/api/image/add/",{
		     method: "POST",
		     headers: { "Auth": this.Auth.refreshToken,
				"type": "post",
				"id": json.post.id 
		     }, 
		     body: data,
		 })
		 const j = await imageAdd.json()
		 json.post.stripped_image = j.stripped_image
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
	     const url = "/api/account/" + key + "/"
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
 .account-header {
     width: 100%;
     display:flex;
     align-items:center;
     flex-direction:column;
 }
.custom-background {
     
 }
</style>
