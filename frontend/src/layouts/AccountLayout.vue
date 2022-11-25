<template>
  <q-layout view="lHh Lpr lFf">
      <div>
	  <h3>{{Profile.username}}</h3>
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
			   <q-btn >Likes {{post.likes.length}}</q-btn>
			   <q-btn @click="showPostComments(post.id)" flat> Comments {{post.comments.length}}</q-btn>
		       </q-card-actions>

		       <div v-if="post.showComments" >
			   <div v-for="comment in post.comments" >
			       <q-card-section>
				   {{ comment.body }}
			       </q-card-section>
			       
			       <q-separator dark />
		       
			       <q-card-actions>
				   <q-btn >Likes {{comment.likes.length}}</q-btn>
			       </q-card-actions>
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
	 }
     }
})
</script>
