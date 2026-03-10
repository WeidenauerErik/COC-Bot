<template>
  <div class="overview">
    <div
      v-for="card in cards"
      :key="card.key"
      class="card"
      :class="`card--${card.cls}`"
    >
      <div class="card-dot" :class="`card-dot--${card.cls}`" />
      <div class="card-body">
        <span class="card-num">{{ stats[card.key] ?? 0 }}</span>
        <span class="card-label">{{ card.label }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  stats: { type: Object, required: true },
})

const cards = [
  { key: 'INFO',    label: 'Info',    cls: 'info'  },
  { key: 'WARNING', label: 'Warning', cls: 'warn'  },
  { key: 'ERROR',   label: 'Error',   cls: 'error' },
  { key: 'DEBUG',   label: 'Debug',   cls: 'debug' },
]
</script>

<style scoped>
.overview {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  padding: 14px 16px;
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  flex-shrink: 0;
}

.card {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  border-radius: var(--radius);
  border: 1px solid var(--border);
  background: var(--surface);
}

.card-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}
.card-dot--info  { background: var(--info); }
.card-dot--warn  { background: var(--warn); }
.card-dot--error { background: var(--error); }
.card-dot--debug { background: var(--debug); }

.card-body {
  display: flex;
  flex-direction: column;
  gap: 1px;
}

.card-num {
  font-family: var(--font-mono);
  font-size: 20px;
  font-weight: 500;
  line-height: 1;
}
.card--info  .card-num { color: var(--info); }
.card--warn  .card-num { color: var(--warn); }
.card--error .card-num { color: var(--error); }
.card--debug .card-num { color: var(--debug); }

.card-label {
  font-size: 11px;
  color: var(--text-2);
}
</style>
