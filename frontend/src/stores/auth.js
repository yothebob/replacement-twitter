import { defineStore } from "pinia";
import { ref, watch } from "vue";
import { computed } from "@vue/reactivity";

export const useAuthStore = defineStore("auth", () => {
  const refreshToken = ref(null);
  const hasAccess = ref(false);

  if (
    localStorage.getItem("refreshToken") &&
    localStorage.getItem("refreshToken") !== undefined
  ) {
    refreshToken.value = JSON.parse(localStorage.getItem("refreshToken"));
  }
  if (
    localStorage.getItem("hasAccess") &&
    localStorage.getItem("hasAccess") !== undefined
  ) {
    hasAccess.value = JSON.parse(localStorage.getItem("hasAccess"));
  }

  watch( hasAccess,
    (hasAccessVal) => {
	localStorage.setItem("hasAccess", JSON.stringify(hasAccessVal));
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
	      this.hasAccess = true;
	  }
      } else { this.hasAccess = false; }
    }
    
    function clearUserSession() {
	this.token = null;
    this.refreshToken = null;
    this.hasAccess = false;
    window.location.href = "/login/";
    return;
  }

  async function validateSession() {
    let url = "/api/token/validate/";
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        access: this.token,
        refresh: this.refreshToken,
      }),
    });
    const json = await res.json();
    if (!res.ok) {
      this.hasAccess = false;
      throw json;
    } else {
      if ("access" in json) {
        this.token = json.access;
        this.hasAccess = true;
      } else {
        this.hasAccess = false;
      }
    }
  }

  return {
    hasAccess,
    refreshToken,
    loginUser,
    validateSession,
    clearUserSession,
  };
});
