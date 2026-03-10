<template>
  <span class="stat-pill" :class="`stat-pill--${levelClass}`">
    <span class="dot" />
    {{ count }}
  </span>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  level: { type: String, required: true },
  count: { type: Number, required: true },
})

const levelClass = computed(() => props.level.toLowerCase().replace('warning', 'warn'))
</script>

<style scoped>
.stat-pill {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 2px 8px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 500;
  font-family: var(--font-mono);
  border: 1px solid transparent;
}

.dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
}

.stat-pill--info {
  background: var(--info-bg);
  border-color: var(--info-border);
  color: var(--info);
}
.stat-pill--info .dot { background: var(--info); }

.stat-pill--warn {
  background: var(--warn-bg);
  border-color: var(--warn-border);
  color: var(--warn);
}
.stat-pill--warn .dot { background: var(--warn); }

.stat-pill--error {
  background: var(--error-bg);
  border-color: var(--error-border);
  color: var(--error);
}
.stat-pill--error .dot { background: var(--error); }
</style>
