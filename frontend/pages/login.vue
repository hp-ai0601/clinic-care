<template>
  <div class="login-screen">
    <form class="card login-card" @submit.prevent="submit">
      <h1>ClinicCare</h1>
      <p>Sign in to view and record consultation notes.</p>

      <p v-if="error" class="alert alert-error">{{ error }}</p>

      <div class="form-row">
        <label>Email</label>
        <input v-model="email" type="email" autocomplete="username" required />
      </div>
      <div class="form-row">
        <label>Password</label>
        <input v-model="password" type="password" autocomplete="current-password" required />
      </div>
      <button class="btn btn-primary" type="submit" :disabled="loading" style="width:100%">
        {{ loading ? "Signing in…" : "Sign in" }}
      </button>
      <p class="demo">Demo: lan@clinic.local / clinic123</p>
    </form>
  </div>
</template>

<script setup>
definePageMeta({ layout: false })

const { post, token } = useApi()
const email = ref("lan@clinic.local")
const password = ref("clinic123")
const loading = ref(false)
const error = ref("")

async function submit() {
  error.value = ""
  loading.value = true
  try {
    const data = await post("/auth/login", {
      email: email.value.trim(),
      password: password.value,
    })
    token.value = data.access_token
    await navigateTo("/consultations")
  } catch (e) {
    error.value = e.data?.detail || "Could not sign in."
  } finally {
    loading.value = false
  }
}
</script>
