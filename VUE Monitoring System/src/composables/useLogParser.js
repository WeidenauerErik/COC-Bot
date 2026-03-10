/**
 * useLogParser
 *
 * Parses log files with format:
 *   [YYYY-MM-DD HH:MM:SS] [LEVEL] Message
 */

export const LOG_LEVELS = ['INFO', 'WARNING', 'ERROR', 'DEBUG']

const LINE_REGEX = /^\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]\s+\[(\w+)\]\s*(.*)/

/**
 * Parse a single raw log line string into a structured object.
 * @param {string} raw
 * @param {number} index  Original line index (0-based)
 * @returns {LogLine}
 */
export function parseLine(raw, index) {
  const match = raw.match(LINE_REGEX)
  if (match) {
    return {
      index,
      timestamp: match[1],
      level: match[2].toUpperCase(),
      message: match[3],
      raw,
    }
  }
  return {
    index,
    timestamp: '',
    level: 'UNKNOWN',
    message: raw,
    raw,
  }
}

/**
 * Count occurrences per log level.
 * @param {LogLine[]} lines
 * @returns {Record<string, number>}
 */
export function buildStats(lines) {
  const stats = { INFO: 0, WARNING: 0, ERROR: 0, DEBUG: 0 }
  for (const line of lines) {
    if (line.level in stats) stats[line.level]++
  }
  return stats
}

/**
 * Determine the severity of a file based on its stats.
 * @returns {'error'|'warning'|'ok'}
 */
export function fileSeverity(stats) {
  if (stats.ERROR > 0)   return 'error'
  if (stats.WARNING > 0) return 'warning'
  return 'ok'
}

/**
 * Read a File object and return a parsed log file descriptor.
 * @param {File} file
 * @returns {Promise<ParsedFile>}
 */
export function parseLogFile(file) {
  return new Promise((resolve) => {
    const reader = new FileReader()
    reader.onload = (e) => {
      const lines = e.target.result
        .split('\n')
        .map((raw, i) => parseLine(raw.trimEnd(), i))
        .filter((l) => l.raw.trim() !== '')

      resolve({
        name: file.name,
        lines,
        stats: buildStats(lines),
        severity: fileSeverity(buildStats(lines)),
      })
    }
    reader.readAsText(file)
  })
}
