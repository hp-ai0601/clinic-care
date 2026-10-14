<template>
  <div>
    <div class="page-head">
      <div>
        <h1>New consultation</h1>
        <p>Record a visit with one or more ICD-10 codes.</p>
      </div>
    </div>

    <form class="card form-card" @submit.prevent="save">
      <p v-if="error" class="alert alert-error">{{ error }}</p>

      <div class="form-row">
        <label>Patient name</label>
        <input v-model="form.patient_name" type="text" maxlength="120" required />
      </div>

      <div class="form-row">
        <label>Diagnosis <span class="hint">— search and add codes</span></label>
        <DiagnosisPicker v-model="form.diagnoses" />
      </div>

      <div class="form-row">
        <label>Treatment notes</label>
        <textarea v-model="form.notes" required placeholder="Findings, plan, follow-up…"></textarea>
      </div>

      <div class="actions">
        <button class="btn btn-primary" type="submit" :disabled="saving">
          {{ saving ? "Saving…" : "Save note" }}
        </button>
        <NuxtLink to="/consultations" class="btn btn-ghost">Cancel</NuxtLink>
      </div>
    </form>
  </div>
</template>

<script setup>
const { post } = useApi()

const form = reactive({
  patient_name: "",
  notes: "",
  diagnoses: [],
})
const saving = ref(false)
const error = ref("")

async function save() {
  error.value = ""
  if (!form.diagnoses.length) {
    error.value = "Add at least one diagnosis code."
    return
  }
  saving.value = true
  try {
    await post("/consultation", {
      patient_name: form.patient_name,
      notes: form.notes,
      diagnosis_codes: form.diagnoses.map((d) => d.code),
    })
    await navigateTo("/consultations")
  } catch (e) {
    const detail = e.data?.detail
    error.value = typeof detail === "string" ? detail : "Could not save the note."
  } finally {
    saving.value = false
  }
}
</script>
