<template>
  <div id="app" class="min-h-screen flex flex-col">
    <!-- Toast for notifications -->
    <Toast position="top-right" />
    
    <!-- Header -->
    <HeaderView />

    <!-- Main Content -->
    <main class="flex-grow container mx-auto px-4 py-8 min-w-[1500px] min-h-[1100px] text-sm">
      <router-view />
    </main>

    <!-- Footer -->
    <FooterView />
  </div>
</template>

<script setup>
import HeaderView from '@/layout/HeaderView.vue'
import FooterView from '@/layout/FooterView.vue'
import Toast from 'primevue/toast'
</script>

<style>
/* Global app styles if needed */
</style>