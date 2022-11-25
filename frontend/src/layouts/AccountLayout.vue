<template>
  <q-layout view="lHh Lpr lFf">
      <div>
	  <h3>{{Profile.username}}</h3>
	  <h5>{{Profile.name}}</h5>
	  <div v-for="post in Profile.posts">
	       <div class="q-pa-md row items-start q-gutter-md">
		   <q-card class="my-card bg-grey-1">
		       <q-card-section>
			   <div class="text-h6">{{post.title}}</div>
			   <div class="text-subtitle2">by {{Profile.username}}</div>
		       </q-card-section>
		       
		       <q-card-section>
			   {{ post.content }}
		       </q-card-section>
		       
		       <q-separator dark />
		       
		       <q-card-actions>
			   <q-btn @click="likeItem(Profile.id, post.id,'post',post)">{{post.liked}} {{post.likes.length}}</q-btn>
			   <q-btn @click="post.showComments = !post.showComments" flat> Comments {{post.comments.length}}</q-btn>
		       </q-card-actions>

		       <div v-if="post.showComments" >
			   <div v-for="comment in post.comments" >
			       <q-card-section>
				   <div>
				       <p>{{comment.account}}</p>
				       <p>
					   {{ comment.body }}
				       </p>
				   </div>
				   <q-btn @click="likeItem(Profile.id, comment.id,'comment',comment)" >like {{comment.likes.length}}</q-btn>
			       </q-card-section>
			       
			       <q-separator dark />
		       
			   </div>
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
	     
	     Profile: {},
	 }
     },
     async created () {
	 this.Profile = await this.getProfilePosts(1);
	 this.Profile.posts.forEach((post) => {
	     // TODO added liked here if userid in post.likes?
	     post.likes.includes(this.Profile.id) ? post.liked = "Liked" : post.liked = "Like"  
	     post.showComments = false;
	 })
     },
     methods: {
	 getProfilePosts: async function (key) {
	     const url = "/api/Account/" + key + "/"
	     const res = await fetch(url, {
		 method: "GET",
		 headers: { "Content-Type": "application/json" }
	     })
	     const json = await res.json();
	     return json;
	 },
	 likeItem: async function (accountKey, itemKey, item, itemObj) {
	     const url = "/api/like/"
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
