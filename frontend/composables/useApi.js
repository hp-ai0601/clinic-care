export function useApi() {
  const config = useRuntimeConfig()
  const base = config.public.apiBase

  function get(path, query) {
    return $fetch(base + path, { query })
  }

  function post(path, body) {
    return $fetch(base + path, { method: "POST", body })
  }

  return { get, post }
}
