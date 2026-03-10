import { ref } from 'vue'

/**
 * useDragDrop
 *
 * Provides drag-and-drop state and handlers for a drop target element.
 * @param {Function} onDrop  Callback receiving the DataTransfer object
 */
export function useDragDrop(onDrop) {
  const isDragging = ref(false)
  let dragCounter = 0

  function handleDragEnter(e) {
    e.preventDefault()
    dragCounter++
    isDragging.value = true
  }

  function handleDragOver(e) {
    e.preventDefault()
  }

  function handleDragLeave() {
    dragCounter--
    if (dragCounter === 0) isDragging.value = false
  }

  async function handleDrop(e) {
    e.preventDefault()
    isDragging.value = false
    dragCounter = 0
    if (onDrop) await onDrop(e.dataTransfer)
  }

  return {
    isDragging,
    handleDragEnter,
    handleDragOver,
    handleDragLeave,
    handleDrop,
  }
}
