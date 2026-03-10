import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { parseLogFile } from '@/composables/useLogParser'

export const useLogsStore = defineStore('logs', () => {
  // ── State ──────────────────────────────────────
  const files = ref([])          // ParsedFile[]
  const activeFilename = ref('') // currently viewed file

  // ── Getters ────────────────────────────────────
  const hasFiles = computed(() => files.value.length > 0)

  const activeFile = computed(() =>
    files.value.find((f) => f.name === activeFilename.value) ?? null
  )

  const totalStats = computed(() => {
    return files.value.reduce(
      (acc, f) => {
        acc.INFO    += f.stats.INFO
        acc.WARNING += f.stats.WARNING
        acc.ERROR   += f.stats.ERROR
        acc.DEBUG   += f.stats.DEBUG
        return acc
      },
      { INFO: 0, WARNING: 0, ERROR: 0, DEBUG: 0 }
    )
  })

  // ── Actions ────────────────────────────────────
  async function loadFromFileList(fileList) {
    const logFiles = Array.from(fileList).filter((f) => f.name.endsWith('.log'))
    if (!logFiles.length) return

    // Sort newest first (filenames are date-based)
    logFiles.sort((a, b) => b.name.localeCompare(a.name))

    const parsed = await Promise.all(logFiles.map(parseLogFile))
    files.value = parsed

    // Auto-select the first (newest) file
    if (parsed.length > 0) {
      activeFilename.value = parsed[0].name
    }
  }

  async function loadFromDropEvent(dataTransfer) {
    const allFiles = []

    async function traverseEntry(entry) {
      if (entry.isFile) {
        await new Promise((res) => entry.file((f) => { allFiles.push(f); res() }))
      } else if (entry.isDirectory) {
        const reader = entry.createReader()
        await new Promise((res) =>
          reader.readEntries(async (entries) => {
            for (const sub of entries) await traverseEntry(sub)
            res()
          })
        )
      }
    }

    for (const item of dataTransfer.items) {
      if (item.kind === 'file') {
        const entry = item.webkitGetAsEntry()
        if (entry) await traverseEntry(entry)
      }
    }

    await loadFromFileList(allFiles)
  }

  function selectFile(filename) {
    activeFilename.value = filename
  }

  function clearAll() {
    files.value = []
    activeFilename.value = ''
  }

  return {
    files,
    activeFilename,
    hasFiles,
    activeFile,
    totalStats,
    loadFromFileList,
    loadFromDropEvent,
    selectFile,
    clearAll,
  }
})
