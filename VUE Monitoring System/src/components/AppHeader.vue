<template>
  <header class="header">
    <RouterLink to="/" class="header-brand">
      <IconFile class="brand-icon" />
      <span class="brand-name">Log Monitor</span>
    </RouterLink>

    <div class="header-meta" v-if="logsStore.hasFiles">
      <span class="file-count">{{ logsStore.files.length }} {{ logsStore.files.length === 1 ? 'Datei' : 'Dateien' }}</span>
      <StatPill level="INFO"    :count="logsStore.totalStats.INFO" />
      <StatPill level="WARNING" :count="logsStore.totalStats.WARNING" />
      <StatPill level="ERROR"   :count="logsStore.totalStats.ERROR" />
    </div>

    <div class="header-actions">
      <button class="btn-ghost" @click="logsStore.clearAll" v-if="logsStore.hasFiles" title="Alle schließen">
        <IconX />
      </button>
      <label class="btn-primary">
        <IconFolderOpen />
        Ordner öffnen
        <input
          type="file"
          webkitdirectory
          multiple
          class="file-input"
          @change="onFileInputChange"
        />
      </label>
    </div>
  </header>
</template>

<script setup>
import { useLogsStore } from '@/stores/logs'
import { useRouter } from 'vue-router'
import StatPill from '@/components/StatPill.vue'
import IconFile from '@/components/icons/IconFile.vue'
import IconFolderOpen from '@/components/icons/IconFolderOpen.vue'
import IconX from '@/components/icons/IconX.vue'

const logsStore = useLogsStore()
const router = useRouter()

async function onFileInputChange(e) {
  await logsStore.loadFromFileList(e.target.files)
  if (logsStore.activeFilename) {
    router.push({ name: 'log', params: { filename: logsStore.activeFilename } })
  }
  // reset so same folder can be re-opened
  e.target.value = ''
}
</script>

<style scoped>
.header {
  height: var(--header-h);
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 0 20px;
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  flex-shrink: 0;
  z-index: 100;
}

.header-brand {
  display: flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
  color: var(--text-1);
}

.brand-icon {
  color: var(--text-2);
  flex-shrink: 0;
}

.brand-name {
  font-size: 14px;
  font-weight: 600;
  letter-spacing: -0.01em;
}

.header-meta {
  display: flex;
  align-items: center;
  gap: 8px;
}

.file-count {
  font-size: 12px;
  color: var(--text-3);
  padding: 2px 8px;
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 20px;
}

.header-actions {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-ghost {
  display: flex;
  align-items: center;
  padding: 6px;
  background: transparent;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  color: var(--text-2);
  transition: all 0.12s;
}
.btn-ghost:hover {
  background: var(--bg);
  color: var(--text-1);
}

.btn-primary {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 7px 14px;
  background: var(--text-1);
  border: none;
  border-radius: var(--radius);
  color: #fff;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: opacity 0.12s;
  position: relative;
}
.btn-primary:hover { opacity: 0.85; }

.file-input {
  position: absolute;
  inset: 0;
  opacity: 0;
  width: 100%;
  cursor: pointer;
}
</style>
