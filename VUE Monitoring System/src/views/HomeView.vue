<template>
  <div class="home">
    <Transition name="fade" mode="out-in">
      <!-- Files loaded but none selected yet -->
      <div v-if="logsStore.hasFiles" class="no-selection">
        <IconFile :size="28" class="no-selection-icon" />
        <p class="no-selection-text">Wähle eine Log-Datei aus der Liste.</p>
      </div>

      <!-- No files at all: show drop zone -->
      <DropZone v-else />
    </Transition>
  </div>
</template>

<script setup>
import { useLogsStore } from '@/stores/logs'
import DropZone from '@/components/DropZone.vue'
import IconFile from '@/components/icons/IconFile.vue'

const logsStore = useLogsStore()
</script>

<style scoped>
.home {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.no-selection {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;
  color: var(--text-3);
}

.no-selection-icon {
  opacity: 0.5;
}

.no-selection-text {
  font-size: 13px;
}
</style>
