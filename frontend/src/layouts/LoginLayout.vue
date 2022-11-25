<template>
  <q-layout view="lHh Lpr lFf">
    
      <div>
	  <h3>Login User</h3><br/>
	<q-input rounded outlined v-model="username" label="Username"/>
	<q-input rounded outlined v-model="password" label="Password"/>
	<q-btn @click="loginUser" color="white" text-color="black" label="Create user" />
    </div>
  </q-layout>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'LoginPage',
  data: () => {
      return {
	  username: '',
	  password: '',
      }
  },
    components: {},
    methods: {
	loginUser: async function () {
	    const url = "/api/login/"
	    const res = await fetch(url, {
		method: "POST",
		headers: { 'Content-Type': 'application/json'},
		body: JSON.stringify({
		    username: this.username,
		    password: this.password
		})
	    });
	    const json = await res.json();
	    return json;
	}
    },
})
</script>
