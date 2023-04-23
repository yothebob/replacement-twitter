<script setup>
 const props = defineProps({
     post: {
	 type: String,
	 description: "the json Object of a post",
     },
     authObj: {
	 type: String,
	 description: "Auth Obj (maybe use Auth.userData)",
     },
     likeItem: {
	 type: String,
	 description: "like item function",
     },
     postShowComments: {
	 type: String,
	 description: "post Show Comments function ",
     }
     
 });

 
</script>
<template>
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
	    <q-btn @click="likeItem(authObj.userId, post.id,'post',post)" :text-color="post.liked" icon="favorite"> {{post.likes.length}}</q-btn>
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
</template>
