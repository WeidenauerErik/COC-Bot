<template>
  <aside class="sidebar" v-if="logsStore.hasFiles">
    <div class="sidebar-header">
      <span class="sidebar-label">Logs</span>
      <input
        v-model="search"
        class="sidebar-search"
        placeholder="Suchen …"
        type="search"
      />
    </div>

    <nav class="sidebar-nav">
      <TransitionGroup name="slide-up" tag="div">
        <FileListItem
          v-for="file in filteredFiles"
          :key="file.name"
          :file="file"
          :active="logsStore.activeFilename === file.name"
          @select="onSelect(file.name)"
        />
      </TransitionGroup>

      <div v-if="filteredFiles.length === 0" class="sidebar-empty">
        Keine Ergebnisse
      </div>
    </nav>
  </aside>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useLogsStore } from '@/stores/logs'
import FileListItem from '@/components/FileListItem.vue'

const logsStore = useLogsStore()
const router = useRouter()
const search = ref('')

const filteredFiles = computed(() => {
  const q = search.value.trim().toLowerCase()
  if (!q) return logsStore.files
  return logsStore.files.filter((f) => f.name.toLowerCase().includes(q))
})

function onSelect(filename) {
  logsStore.selectFile(filename)
  router.push({ name: 'log', params: { filename } })
}
</script>

<style scoped>
.sidebar {
  width: var(--sidebar-w);
  background: var(--surface);
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  flex-shrink: 0;
}

.sidebar-header {
  padding: 12px;
  border-bottom: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex-shrink: 0;
}

.sidebar-label {
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--text-3);
}

.sidebar-search {
  width: 100%;
  padding: 6px 10px;
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  color: var(--text-1);
  font-size: 12px;
  outline: none;
  transition: border-color 0.12s;
  appearance: none;
}
.sidebar-search::placeholder { color: var(--text-3); }
.sidebar-search:focus { border-color: var(--border-2); }

.sidebar-nav {
  flex: 1;
  overflow-y: auto;
  padding: 6px;
}

.sidebar-empty {
  padding: 24px 12px;
  text-align: center;
  color: var(--text-3);
  font-size: 12px;
}
</style>
