export default defineNuxtRouteMiddleware((to) => {
  const token = useCookie("clinic_token")
  if (to.path === "/login") {
    if (token.value) return navigateTo("/consultations")
    return
  }
  if (!token.value) return navigateTo("/login")
})
