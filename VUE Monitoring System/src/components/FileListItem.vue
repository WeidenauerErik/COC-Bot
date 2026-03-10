<template>
  <button
    class="file-item"
    :class="{ 'file-item--active': active }"
    @click="$emit('select')"
  >
    <span class="severity-dot" :class="`severity-dot--${file.severity}`" />

    <div class="file-info">
      <span class="file-name">{{ file.name }}</span>
      <span class="file-meta">{{ file.lines.length }} Zeilen</span>
    </div>

    <div class="file-badges">
      <span v-if="file.stats.ERROR > 0"   class="badge badge--error">{{ file.stats.ERROR }}</span>
      <span v-if="file.stats.WARNING > 0" class="badge badge--warn">{{ file.stats.WARNING }}</span>
    </div>
  </button>
</template>

<script setup>
defineProps({
  file:   { type: Object,  required: true },
  active: { type: Boolean, default: false },
})
defineEmits(['select'])
</script>

<style scoped>
.file-item {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  padding: 8px 10px;
  border-radius: var(--radius);
  border: 1px solid transparent;
  background: transparent;
  text-align: left;
  cursor: pointer;
  transition: background 0.1s, border-color 0.1s;
  margin-bottom: 1px;
}
.file-item:hover {
  background: var(--bg);
}
.file-item--active {
  background: var(--bg);
  border-color: var(--border);
}

.severity-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  flex-shrink: 0;
}
.severity-dot--ok      { background: #22c55e; }
.severity-dot--warning { background: var(--warn); }
.severity-dot--error   { background: var(--error); }

.file-info {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 1px;
}

.file-name {
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 500;
  color: var(--text-1);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.file-item--active .file-name {
  color: var(--info);
}

.file-meta {
  font-size: 11px;
  color: var(--text-3);
}

.file-badges {
  display: flex;
  gap: 3px;
  flex-shrink: 0;
}

.badge {
  font-family: var(--font-mono);
  font-size: 10px;
  font-weight: 500;
  padding: 1px 5px;
  border-radius: var(--radius-sm);
}
.badge--error { background: var(--error-bg); color: var(--error); }
.badge--warn  { background: var(--warn-bg);  color: var(--warn); }
</style>
