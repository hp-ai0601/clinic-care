export function useApi() {
  const config = useRuntimeConfig()
  const token = useCookie("clinic_token")
  const base = config.public.apiBase

  function headers() {
    const h = {}
    if (token.value) h.Authorization = `Bearer ${token.value}`
    return h
  }

  async function request(path, opts = {}) {
    try {
      return await $fetch(base + path, {
        ...opts,
        headers: { ...headers(), ...(opts.headers || {}) },
      })
    } catch (err) {
      if (err.status === 401 && path !== "/auth/login") {
        token.value = null
        await navigateTo("/login")
      }
      throw err
    }
  }

  function get(path, query) {
    return request(path, { query })
  }

  function post(path, body) {
    return request(path, { method: "POST", body })
  }

  return { get, post, token }
}
