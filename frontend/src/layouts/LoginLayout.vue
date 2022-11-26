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
	      <q-input rounded outlined v-model="username" label="Username"/>
	      <q-input rounded outlined v-model="password" label="Password"/>
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
	  password: '',
      }
     },
     components: {},

     async created() {
	 this.Auth = useAuthStore();
     },
     methods: {
	 loginUser: async function () {
	     const res = await this.Auth.loginUser(this.username, this.password)
	     if (this.Auth.hasAccess && this.Auth.refreshToken) {
		 window.location.href = "/account";
	     }
	 }
     },
 })
</script>
