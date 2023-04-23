<script setup>
 import { useRouter } from 'vue-router';
 import { ref, onMounted, reactive } from 'vue';
 import { useAuthStore } from '../stores/auth';
 import { useQuasar } from 'quasar'

 
 const router = useRouter();
 const authStore = useAuthStore();
 const store = reactive({
     showNotes: false,
     notes: [],
 });
 const $q = useQuasar();
 
 onMounted(() => {
     store.notes = authStore.notificationStack
     setInterval(async () => {
	 store.notes = await authStore.checkNotifications();
     }, 5000);
 })

 const show = () => {
     if (store.showNotes) {
	 console.log("set false")
	 store.showNotes = false
     } else {
	 store.showNotes = true
	 if ("notifications" in store.notes) {
	     store.notes.notifications.forEach((no) => {
		 console.log(no.message)
		 $q.notify({
		     message: no.message,
		     actions: [{
			 label: "Dismiss",
			 handler: () => {
			     authStore.clickNotificationStack(no.id);
			     store.notes.notifications = store.notes.notifications.filter((nt) => {nt.id != no.id})}
		     }]
		 })
	     })
	 }
     }
 }

</script>
<template>
    <q-btn color="blue"
	   @click="show"
    >
	Notifications
	<q-badge v-show="'notifications' in  store.notes? store.notes.notifications.length > 0 : false" color="red" rounded floating :label="'notifications' in store.notes? store.notes.notifications.length : ''" />
    </q-btn>
</template>

