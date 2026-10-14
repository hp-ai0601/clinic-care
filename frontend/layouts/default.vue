<template>
  <div>
    <header class="topbar">
      <NuxtLink to="/consultations" class="brand">
        ClinicCare <span>Mini EMR</span>
      </NuxtLink>
      <nav class="nav">
        <NuxtLink to="/consultations">Consultations</NuxtLink>
        <NuxtLink to="/consultations/new">New note</NuxtLink>
        <NuxtLink to="/search">Search</NuxtLink>
      </nav>
      <div class="topbar-right">
        <span>{{ doctor?.name }}</span>
        <button class="linkish" type="button" @click="logout">Sign out</button>
      </div>
    </header>
    <main class="wrap">
      <slot />
    </main>
  </div>
</template>

<script setup>
const { get, token } = useApi()
const doctor = ref(null)

if (token.value) {
  try {
    doctor.value = await get("/auth/me")
  } catch {
    doctor.value = null
  }
}

function logout() {
  token.value = null
  navigateTo("/login")
}
</script>
