<template>
  <div class="log-view" v-if="file">
    <!-- Overview stats -->
    <OverviewCards :stats="file.stats" />

    <!-- Toolbar with filters + search -->
    <LogToolbar
      :filename="file.name"
      :stats="file.stats"
      :total-lines="file.lines.length"
      :filtered-count="filteredLines.length"
      v-model:model-level="activeLevel"
      v-model:model-search="searchQuery"
    />

    <!-- Log lines -->
    <div class="lines-container" ref="linesContainer">
      <template v-if="filteredLines.length > 0">
        <LogLine
          v-for="line in filteredLines"
          :key="line.index"
          :line="line"
          :search-query="searchQuery"
        />
      </template>

      <div v-else class="empty-state">
        Keine Einträge für diesen Filter.
      </div>
    </div>
  </div>

  <!-- File not found -->
  <div v-else class="not-found">
    <p>Datei <code>{{ filename }}</code> nicht gefunden.</p>
    <RouterLink to="/" class="back-link">← Zurück</RouterLink>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { useLogsStore } from '@/stores/logs'
import { useLogFilter } from '@/composables/useLogFilter'
import OverviewCards from '@/components/OverviewCards.vue'
import LogToolbar from '@/components/LogToolbar.vue'
import LogLine from '@/components/LogLine.vue'

const props = defineProps({
  filename: { type: String, required: true },
})

const logsStore = useLogsStore()
const linesContainer = ref(null)

// Keep store in sync with the route param
watch(
  () => props.filename,
  (name) => { logsStore.selectFile(name) },
  { immediate: true }
)

const file = computed(() => logsStore.activeFile)

// Filter composable over the active file's lines
const fileLines = computed(() => file.value?.lines ?? [])
const { activeLevel, searchQuery, filteredLines } = useLogFilter(fileLines)

// Scroll to top when file or filter changes
watch([filteredLines], () => {
  if (linesContainer.value) linesContainer.value.scrollTop = 0
})
</script>

<style scoped>
.log-view {
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
}

.lines-container {
  flex: 1;
  overflow-y: auto;
  background: var(--surface);
}

.empty-state {
  padding: 40px;
  text-align: center;
  color: var(--text-3);
  font-size: 13px;
}

.not-found {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  color: var(--text-2);
  font-size: 13px;
}

.not-found code {
  font-family: var(--font-mono);
  background: var(--bg);
  padding: 2px 6px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border);
}

.back-link {
  color: var(--info);
  text-decoration: none;
  font-size: 12px;
}
.back-link:hover { text-decoration: underline; }
</style>
