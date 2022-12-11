import { defineStore } from "pinia";
import { ref, watch } from "vue";
import { computed } from "@vue/reactivity";
import { useQuasar } from 'quasar';

export const useAuthStore = defineStore("auth", () => {
    const refreshToken = ref(null);
    const following = ref(null);
    const hasAccess = ref(false);
    const userId = ref(null);
    const userData = ref(null);
    const darkMode = ref(false);
    const $q = useQuasar();
    
  if (
    localStorage.getItem("refreshToken") &&
    localStorage.getItem("refreshToken") !== undefined
  ) {
    refreshToken.value = JSON.parse(localStorage.getItem("refreshToken"));
  }
  if (
    localStorage.getItem("following") &&
    localStorage.getItem("following") !== undefined
  ) {
    following.value = JSON.parse(localStorage.getItem("following"));
  }
  if (
    localStorage.getItem("userData") &&
    localStorage.getItem("userData") !== undefined
  ) {
    userData.value = JSON.parse(localStorage.getItem("userData"));
  }
  if (
    localStorage.getItem("userId") &&
    localStorage.getItem("userId") !== undefined
  ) {
    userId.value = JSON.parse(localStorage.getItem("userId"));
  }
  if (
    localStorage.getItem("hasAccess") &&
    localStorage.getItem("hasAccess") !== undefined
  ) {
    hasAccess.value = JSON.parse(localStorage.getItem("hasAccess"));
  }
  if (
    localStorage.getItem("darkMode") &&
    localStorage.getItem("darkMode") !== undefined
  ) {
    darkMode.value = JSON.parse(localStorage.getItem("darkMode"));
  }

  watch( hasAccess,
    (hasAccessVal) => {
	localStorage.setItem("hasAccess", JSON.stringify(hasAccessVal));
    },
    { deep: true }
  );
  watch( darkMode,
    (darkModeVal) => {
	localStorage.setItem("darkMode", JSON.stringify(darkModeVal));
    },
    { deep: true }
  );
  watch( userId,
    (userIdVal) => {
	localStorage.setItem("userId", JSON.stringify(userIdVal));
    },
    { deep: true }
  );
  watch(
    refreshToken,
    (refreshVal) => {
      localStorage.setItem("refreshToken", JSON.stringify(refreshVal));
    },
    { deep: true }
  );
  watch(
    following,
    (refreshVal) => {
      localStorage.setItem("following", JSON.stringify(refreshVal));
    },
    { deep: true }
  );
  watch(
    userData,
    (refreshVal) => {
      localStorage.setItem("userData", JSON.stringify(refreshVal));
    },
    { deep: true }
  );

    function setDarkMode() {
	this.darkMode = !this.darkMode;
	$q.dark.set(this.darkMode);
    }
    
    async function loginUser(username, password) {
    let url = "/api/login/";
      const res = await fetch(url, {
	  method: "POST",
	  headers: { "Content-Type": "application/json" },
	  body: JSON.stringify({
	      username: username,
              password: password,
	  })
      })
      const json = await res.json();
      if (res.ok) {
	  if ( "refresh" in json ) {
	      this.refreshToken = json.refresh;
	      this.userId = json.id;
	      this.hasAccess = true;
	      this.following = json.auth.following;
	      this.userData = json.auth;
	  }
      } else { this.hasAccess = false; }
    }
    
    function clearUserSession() {
	localStorage.clear();
	window.location.href = "/login/";
	return;
  }

  async function validateSession() {
    let url = "/api/validate/";
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        refresh: this.refreshToken,
      }),
    });
    const json = await res.json();
    if (!res.ok) {
      this.hasAccess = false;
      throw json;
    } else {
      if ("success" in json) {
        this.hasAccess = true;
      } else {
        this.hasAccess = false;
	  location.href = "/login";
      }
    }
  }

  return {
    userId,
    userData,
    hasAccess,
    refreshToken,
    following,
    loginUser,
    validateSession,
    clearUserSession,
      setDarkMode,
  };
});
