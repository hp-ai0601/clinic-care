<template>
  <div>
    <div class="page-head">
      <div>
        <h1>Search notes</h1>
        <p>Filter by patient name or ICD-10 code / description.</p>
      </div>
    </div>

    <form class="card search-bar" @submit.prevent="run">
      <div class="form-row">
        <label>Patient</label>
        <input v-model="patient" type="text" placeholder="e.g. Nguyen" />
      </div>
      <div class="form-row">
        <label>Diagnosis</label>
        <input v-model="diagnosis" type="text" placeholder="e.g. E11 or diabetes" />
      </div>
      <button class="btn btn-primary" type="submit" :disabled="pending">Search</button>
    </form>

    <p v-if="error" class="alert alert-error">Search failed. Is the API running?</p>
    <ConsultationTable
      v-else-if="searched && !pending"
      :rows="rows || []"
      empty-text="No notes matched that search."
    />
  </div>
</template>

<script setup>
const { get } = useApi()
const patient = ref("")
const diagnosis = ref("")
const searched = ref(false)
const pending = ref(false)
const error = ref(null)
const rows = ref([])

async function run() {
  pending.value = true
  error.value = null
  searched.value = true
  try {
    rows.value = await get("/consultation", {
      patient: patient.value.trim() || undefined,
      diagnosis: diagnosis.value.trim() || undefined,
    })
  } catch (e) {
    error.value = e
  } finally {
    pending.value = false
  }
}
</script>
