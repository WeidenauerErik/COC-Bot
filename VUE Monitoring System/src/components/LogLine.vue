<template>
  <div class="log-line" :class="`log-line--${levelClass}`">
    <span class="col-num">{{ line.index + 1 }}</span>
    <span class="col-ts">{{ line.timestamp }}</span>
    <span class="col-level">{{ line.level }}</span>
    <span class="col-msg" v-html="highlightedMessage" />
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  line:        { type: Object, required: true },
  searchQuery: { type: String, default: '' },
})

const levelClass = computed(() => {
  const map = {
    INFO:    'info',
    WARNING: 'warn',
    ERROR:   'error',
    DEBUG:   'debug',
  }
  return map[props.line.level] ?? 'unknown'
})

function escHtml(str) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
}

const highlightedMessage = computed(() => {
  const escaped = escHtml(props.line.message)
  const q = props.searchQuery.trim()
  if (!q) return escaped
  const safe = escHtml(q)
  const regex = new RegExp(`(${safe.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi')
  return escaped.replace(regex, '<mark class="highlight">$1</mark>')
})
</script>

<style>
/* global so v-html mark works */
mark.highlight {
  background: #fef08a;
  color: #78350f;
  border-radius: 2px;
  padding: 0 1px;
}
</style>

<style scoped>
.log-line {
  display: grid;
  grid-template-columns: 48px 158px 74px 1fr;
  border-bottom: 1px solid var(--border);
  transition: background 0.07s;
  font-family: var(--font-mono);
  font-size: 12px;
}
.log-line:hover { background: var(--surface-2); }

/* accent bar */
.log-line--warn    { border-left: 2px solid var(--warn); }
.log-line--error   { border-left: 2px solid var(--error); }
.log-line--debug   { border-left: 2px solid var(--debug); }
.log-line--info,
.log-line--unknown { border-left: 2px solid transparent; }

.col-num {
  padding: 5px 8px 5px 10px;
  color: var(--text-3);
  font-size: 10px;
  text-align: right;
  user-select: none;
  border-right: 1px solid var(--border);
}

.col-ts {
  padding: 5px 10px;
  color: var(--text-3);
  white-space: nowrap;
  border-right: 1px solid var(--border);
}

.col-level {
  padding: 5px 8px;
  font-size: 10px;
  font-weight: 500;
  text-align: center;
  border-right: 1px solid var(--border);
}
.log-line--info  .col-level { color: var(--info); }
.log-line--warn  .col-level { color: var(--warn); }
.log-line--error .col-level { color: var(--error); }
.log-line--debug .col-level { color: var(--debug); }
.log-line--unknown .col-level { color: var(--text-3); }

.col-msg {
  padding: 5px 12px;
  color: var(--text-1);
  word-break: break-word;
  white-space: pre-wrap;
}
.log-line--warn  .col-msg { color: #92400e; }
.log-line--error .col-msg { color: #991b1b; }
.log-line--debug .col-msg { color: #5b21b6; }
</style>
