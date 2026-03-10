<template>
  <div class="toolbar">
    <span class="filename">{{ filename }}</span>
    <div class="sep" />

    <!-- Level filters -->
    <button
      class="filter-btn"
      :class="{ 'filter-btn--active-all': modelLevel === 'ALL' }"
      @click="$emit('update:modelLevel', 'ALL')"
    >
      Alle <span class="count">{{ totalLines }}</span>
    </button>

    <button
      v-for="f in filters"
      :key="f.key"
      class="filter-btn"
      :class="[`filter-btn--${f.cls}`, { 'filter-btn--active': modelLevel === f.key }]"
      @click="$emit('update:modelLevel', f.key)"
    >
      {{ f.label }} <span class="count">{{ stats[f.key] ?? 0 }}</span>
    </button>

    <div class="spacer" />

    <!-- Search -->
    <div class="search-wrap">
      <IconSearch class="search-icon" />
      <input
        :value="modelSearch"
        @input="$emit('update:modelSearch', $event.target.value)"
        class="search-input"
        placeholder="Suchen …"
        type="search"
      />
    </div>

    <span class="result-count">{{ filteredCount }} Zeilen</span>
  </div>
</template>

<script setup>
import IconSearch from '@/components/icons/IconSearch.vue'

defineProps({
  filename:      { type: String, required: true },
  stats:         { type: Object, required: true },
  totalLines:    { type: Number, required: true },
  filteredCount: { type: Number, required: true },
  modelLevel:    { type: String, default: 'ALL' },
  modelSearch:   { type: String, default: '' },
})

defineEmits(['update:modelLevel', 'update:modelSearch'])

const filters = [
  { key: 'INFO',    label: 'Info',    cls: 'info'  },
  { key: 'WARNING', label: 'Warning', cls: 'warn'  },
  { key: 'ERROR',   label: 'Error',   cls: 'error' },
  { key: 'DEBUG',   label: 'Debug',   cls: 'debug' },
]
</script>

<style scoped>
.toolbar {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 16px;
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  flex-shrink: 0;
  flex-wrap: wrap;
}

.filename {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--text-2);
}

.sep {
  width: 1px;
  height: 16px;
  background: var(--border);
  margin: 0 2px;
  flex-shrink: 0;
}

.spacer { flex: 1; }

.filter-btn {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 4px 10px;
  border-radius: 6px;
  border: 1px solid var(--border);
  background: transparent;
  color: var(--text-2);
  font-size: 11px;
  font-weight: 500;
  transition: all 0.1s;
}
.filter-btn:hover {
  background: var(--bg);
  color: var(--text-1);
}

.filter-btn--active-all {
  background: var(--text-1);
  border-color: var(--text-1);
  color: #fff;
}

.filter-btn--info.filter-btn--active {
  background: var(--info-bg);
  border-color: var(--info-border);
  color: var(--info);
}
.filter-btn--warn.filter-btn--active {
  background: var(--warn-bg);
  border-color: var(--warn-border);
  color: var(--warn);
}
.filter-btn--error.filter-btn--active {
  background: var(--error-bg);
  border-color: var(--error-border);
  color: var(--error);
}
.filter-btn--debug.filter-btn--active {
  background: var(--debug-bg);
  border-color: var(--debug-border);
  color: var(--debug);
}

.count {
  font-family: var(--font-mono);
  font-size: 10px;
  opacity: 0.7;
}

.search-wrap {
  position: relative;
  display: flex;
  align-items: center;
}
.search-icon {
  position: absolute;
  left: 8px;
  color: var(--text-3);
  pointer-events: none;
}
.search-input {
  padding: 5px 10px 5px 28px;
  width: 200px;
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  color: var(--text-1);
  font-size: 12px;
  outline: none;
  appearance: none;
  transition: border-color 0.12s;
}
.search-input::placeholder { color: var(--text-3); }
.search-input:focus { border-color: var(--border-2); }

.result-count {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--text-3);
}
</style>
