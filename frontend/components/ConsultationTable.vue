<template>
  <div class="card">
    <div v-if="!rows.length" class="empty">{{ emptyText }}</div>
    <table v-else>
      <thead>
        <tr>
          <th>Date</th>
          <th>Patient</th>
          <th>Diagnosis</th>
          <th>Notes</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="row in rows" :key="row.id">
          <td class="muted">{{ formatDate(row.created_at) }}</td>
          <td>{{ row.patient_name }}</td>
          <td>
            <span v-for="dx in row.diagnoses" :key="dx.code" class="chip" :title="dx.description">
              {{ dx.code }}
            </span>
          </td>
          <td class="notes-preview">{{ row.notes }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
defineProps({
  rows: { type: Array, default: () => [] },
  emptyText: { type: String, default: "No consultation notes yet." },
})

function formatDate(value) {
  if (!value) return ""
  return new Date(value).toLocaleString()
}
</script>
