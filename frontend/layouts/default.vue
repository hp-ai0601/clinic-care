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
    </header>
    <main class="wrap">
      <slot />
    </main>
  </div>
</template>
