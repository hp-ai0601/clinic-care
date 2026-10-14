<template>
  <div>
    <div class="page-head">
      <div>
        <h1>Consultations</h1>
        <p>Past notes, newest first.</p>
      </div>
      <NuxtLink to="/consultations/new" class="btn btn-primary">New consultation</NuxtLink>
    </div>
    <p v-if="error" class="alert alert-error">Could not load notes. Is the API running?</p>
    <ConsultationTable v-else-if="!pending" :rows="rows || []" />
    <p v-else class="muted">Loading…</p>
  </div>
</template>

<script setup>
const { get } = useApi()
const { data: rows, pending, error, refresh } = await useAsyncData("consultations", () => get("/consultation"))
onMounted(() => refresh())
</script>
