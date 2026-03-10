import { ref, computed } from 'vue'

/**
 * useLogFilter
 *
 * Provides reactive filtering and search over an array of log lines.
 * @param {Ref<LogLine[]>} lines
 */
export function useLogFilter(lines) {
  const activeLevel = ref('ALL')
  const searchQuery = ref('')

  const filteredLines = computed(() => {
    let result = lines.value ?? []

    if (activeLevel.value !== 'ALL') {
      result = result.filter((l) => l.level === activeLevel.value)
    }

    const q = searchQuery.value.trim().toLowerCase()
    if (q) {
      result = result.filter(
        (l) =>
          l.message.toLowerCase().includes(q) ||
          l.timestamp.includes(q)
      )
    }

    return result
  })

  function setLevel(level) {
    activeLevel.value = level
  }

  function resetFilter() {
    activeLevel.value = 'ALL'
    searchQuery.value = ''
  }

  return {
    activeLevel,
    searchQuery,
    filteredLines,
    setLevel,
    resetFilter,
  }
}
