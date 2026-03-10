<template>
  <div
    class="drop-zone"
    :class="{ 'drop-zone--active': isDragging }"
    @dragenter="handleDragEnter"
    @dragover="handleDragOver"
    @dragleave="handleDragLeave"
    @drop="handleDrop"
  >
    <div class="drop-box">
      <div class="drop-icon-wrap">
        <IconFolder class="drop-icon" />
      </div>
      <h2 class="drop-title">logs/ Ordner hier ablegen</h2>
      <p class="drop-sub">
        Ziehe deinen <code>logs/</code> Ordner in dieses Fenster<br />
        oder wähle ihn über den Button oben rechts aus.
      </p>
    </div>
  </div>
</template>

<script setup>
import { useLogsStore } from '@/stores/logs'
import { useDragDrop } from '@/composables/useDragDrop'
import { useRouter } from 'vue-router'
import IconFolder from '@/components/icons/IconFolder.vue'

const logsStore = useLogsStore()
const router = useRouter()

async function onDrop(dataTransfer) {
  await logsStore.loadFromDropEvent(dataTransfer)
  if (logsStore.activeFilename) {
    router.push({ name: 'log', params: { filename: logsStore.activeFilename } })
  }
}

const { isDragging, handleDragEnter, handleDragOver, handleDragLeave, handleDrop } =
  useDragDrop(onDrop)
</script>

<style scoped>
.drop-zone {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
  transition: background 0.15s;
}
.drop-zone--active {
  background: #f0f4ff;
}

.drop-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 14px;
  padding: 56px 64px;
  background: var(--surface);
  border: 1.5px dashed var(--border-2);
  border-radius: var(--radius-lg);
  text-align: center;
  transition: border-color 0.15s;
  max-width: 400px;
}
.drop-zone--active .drop-box {
  border-color: var(--info);
}

.drop-icon-wrap {
  width: 48px;
  height: 48px;
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  display: flex;
  align-items: center;
  justify-content: center;
}
.drop-icon {
  color: var(--text-2);
}

.drop-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-1);
  letter-spacing: -0.01em;
}

.drop-sub {
  font-size: 13px;
  color: var(--text-2);
  line-height: 1.7;
}

.drop-sub code {
  font-family: var(--font-mono);
  font-size: 12px;
  background: var(--bg);
  padding: 1px 5px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border);
  color: var(--text-1);
}
</style>
