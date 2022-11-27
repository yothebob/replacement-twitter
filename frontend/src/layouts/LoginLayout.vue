<template>
  <q-layout view="lHh Lpr lFf">
      <div v-if="pageType == 'login'">
	  <div>
	      <h3>Login User</h3><br/>
	      <q-input rounded outlined v-model="username" label="Username"/>
	      <q-input rounded outlined v-model="password" label="Password"/>
	      <div style="display:flex;justify-contents:space-between;">
		  <q-btn @click="loginUser" color="white" text-color="black" label="Login user" />
		  <q-btn @click="pageType='create'" color="white" text-color="black" label="create account" />
	      </div>
	  </div>
      </div>
      <div v-else-if="pageType == 'create'">
	  <div>
	      <h3>Create User</h3><br/>
	      <q-input rounded outlined v-model="username1" label="Username"/>
	      <q-input rounded outlined v-model="namez" label="name"/>
	      <q-input rounded outlined v-model="password1" label="Password" type="password"/>
	      <q-input rounded outlined v-model="passwordAgain" type="password" label="Password Again"/>
	      <q-select v-model="postColor" :options="colorOptions" label="Post Color" />
	      <div style="display:flex;justify-contents:space-between;">
		  <q-btn @click="loginUser" color="white" text-color="black" label="Create user" />
		  <q-btn @click="pageType='login'" color="white" text-color="black" label="Have account? login" />
	      </div>
	  </div>
	  
      </div>
  </q-layout>
</template>

<script>
 import { defineComponent } from 'vue';
 import { useAuthStore } from '../stores/auth';


 export default defineComponent({
     name: 'LoginPage',
     
     data: () => {
	 return {
	     pageType: "login",
	     Auth: null,
	     username: '',
	     username1: '',
	     namez: '',
	     password: '',
	     password1: '',
	     passwordAgain: '',
	     postColor: '',
	     colorOptions: [],
	     
	 }
     },
     components: {},

     async created() {
	 this.Auth = useAuthStore();
	 this.colorOptions = [
	     "white",
	     "red",
	     "blue",
	     "green",
	     "purple",
	     "pink",
	 ];
     },
     methods: {
	 loginUser: async function () {
	     const res = await this.Auth.loginUser(this.username, this.password)
	     if (this.Auth.hasAccess && this.Auth.refreshToken) {
		 window.location.href = "/account/" + this.Auth.userId ;
	     }
	 }
	 /* createUser: async function () {
	    console.log("hi")
	    const url = "/api";
	    const res = await fetch(url, {
	    method: "POST",
	    headers: { "Content-Type": "application/json" },
	    body: JSON.stringify({
	    username: this.username1,
	    namez: this.namez,
	    password: this.password1,
	    passwordAgain: this.passwordAgain,
	    postColor: this.postColor,
	    })
	    })
	    const json = await res.json();
	    }, */
     },
 })
</script>
