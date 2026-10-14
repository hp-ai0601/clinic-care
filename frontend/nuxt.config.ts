export default defineNuxtConfig({
  css: ["~/assets/css/main.css"],
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || "http://127.0.0.1:8000",
    },
  },
  app: {
    head: {
      title: "ClinicCare",
      meta: [{ name: "viewport", content: "width=device-width, initial-scale=1" }],
    },
  },
})
