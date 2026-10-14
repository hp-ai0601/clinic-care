<template>
  <div class="picker">
    <input
      v-model="term"
      type="text"
      placeholder="Type a code or description, e.g. E11 or hypertension"
      @focus="onFocus"
      @keydown.esc="open = false"
    />
    <div v-if="open && results.length" class="picker-list">
      <button
        v-for="item in results"
        :key="item.code"
        type="button"
        class="picker-item"
        @mousedown.prevent="add(item)"
      >
        <strong>{{ item.code }}</strong>
        <span>{{ item.description }}</span>
      </button>
    </div>
    <div v-if="modelValue.length" class="selected">
      <span v-for="item in modelValue" :key="item.code" class="chip">
        {{ item.code }}
        <button type="button" @click="remove(item.code)" aria-label="Remove">×</button>
      </span>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  modelValue: { type: Array, default: () => [] },
})
const emit = defineEmits(["update:modelValue"])

const { get } = useApi()
const term = ref("")
const results = ref([])
const open = ref(false)
let timer = null

watch(term, (value) => {
  clearTimeout(timer)
  timer = setTimeout(() => lookup(value), 220)
})

async function lookup(value) {
  const q = value.trim()
  if (!q) {
    results.value = []
    open.value = false
    return
  }
  const selected = new Set(props.modelValue.map((d) => d.code))
  try {
    const rows = await get("/diagnosis", { search: q })
    results.value = rows.filter((d) => !selected.has(d.code))
    open.value = results.value.length > 0
  } catch {
    results.value = []
  }
}

function onFocus() {
  if (term.value.trim()) lookup(term.value)
}

function add(item) {
  if (props.modelValue.some((d) => d.code === item.code)) return
  emit("update:modelValue", [...props.modelValue, item])
  term.value = ""
  results.value = []
  open.value = false
}

function remove(code) {
  emit(
    "update:modelValue",
    props.modelValue.filter((d) => d.code !== code),
  )
}
</script>
