import { computed, onBeforeUnmount, onMounted, ref } from 'vue'

/* ---------- long-press (mobile) opens the same menu as the desktop ⋮ ---------- */
const EXCLUDE_SEL = 'select, input, button, .move-overlay, .grip'
const LONG_PRESS_MS = 480
const MOVE_CANCEL_PX = 10

export function useListSession({
  list, // Ref<Array> — the flat items array (contains section: marker rows); mutated in place
  rootEl, // Ref<HTMLElement> — container for DOM queries + event listeners
  isDesktop, // Ref<boolean>
  persistReorder, // (item, newIndex) => any — persists an item's new index
  isMarker = (it) => typeof it?.name === 'string' && it.name.startsWith('section:'),
  isSectionLocked = () => false, // (marker) => boolean — locked sections are excluded from reordering (buttons + drag)
  onOutsideClick // optional (target) => boolean — return true if it handled an outside click
}) {
  const editingItemId = ref(null)
  const editingSectionId = ref(null)
  const movingItemId = ref(null)
  const movingSectionId = ref(null)
  const sectionPickerItemId = ref(null)

  const groupedItems = computed(() => {
    const groups = []
    let current = { marker: null, items: [] }
    for (const it of list.value || []) {
      if (isMarker(it)) {
        groups.push(current)
        current = { marker: it, items: [] }
      } else {
        current.items.push(it)
      }
    }
    groups.push(current)
    return groups
  })

  function reorderableSections() {
    return groupedItems.value.filter((g) => g.marker && !isSectionLocked(g.marker))
  }

  function isFirstSection(marker) {
    const groups = reorderableSections()
    return groups[0]?.marker.id === marker.id
  }
  function isLastSection(marker) {
    const groups = reorderableSections()
    return groups[groups.length - 1]?.marker.id === marker.id
  }

  function rebuildFlatWithReorderedSections(reorderedReorderable) {
    const groups = groupedItems.value
    const reorderedIds = new Set(reorderedReorderable.map((g) => g.marker.id))
    let ri = 0
    const flat = []
    for (const g of groups) {
      if (!g.marker) {
        flat.push(...g.items)
      } else if (reorderedIds.has(g.marker.id)) {
        const next = reorderedReorderable[ri++]
        flat.push(next.marker, ...next.items)
      } else {
        flat.push(g.marker, ...g.items)
      }
    }
    return flat
  }

  function toggleItemOverlay(id) {
    movingItemId.value = movingItemId.value === id ? null : id
    sectionPickerItemId.value = null
  }
  function closeItemOverlay() {
    movingItemId.value = null
    sectionPickerItemId.value = null
  }
  function toggleSectionOverlay(id) {
    movingSectionId.value = movingSectionId.value === id ? null : id
  }
  function openEdit(id) {
    movingItemId.value = null
    sectionPickerItemId.value = null
    editingSectionId.value = null
    editingItemId.value = id
  }

  function openEditSection(id) {
    editingItemId.value = null
    movingItemId.value = null
    movingSectionId.value = null
    sectionPickerItemId.value = null
    editingSectionId.value = id
  }

  function closeEditSection() {
    editingSectionId.value = null
  }

  function openSort(id) {
    editingItemId.value = null
    editingSectionId.value = null
    movingItemId.value = id
    movingSectionId.value = null
    sectionPickerItemId.value = null
  }

  function openSortSection(id) {
    editingItemId.value = null
    editingSectionId.value = null
    movingItemId.value = null
    sectionPickerItemId.value = null
    movingSectionId.value = id
  }

  function closeEdit() {
    editingItemId.value = null
  }

  function closeSession() {
    editingItemId.value = null
    editingSectionId.value = null
    movingItemId.value = null
    movingSectionId.value = null
    sectionPickerItemId.value = null
  }

  function setSessionMode(mode) {
    const currentSectionId = editingSectionId.value ?? movingSectionId.value
    if (currentSectionId !== null) {
      if (mode === 'edit') openEditSection(currentSectionId)
      else openSortSection(currentSectionId)
      return
    }
    const currentItemId = editingItemId.value ?? movingItemId.value
    if (currentItemId === null) return
    if (mode === 'edit') openEdit(currentItemId)
    else openSort(currentItemId)
  }

  function onRowClick(item) {
    if (editingItemId.value !== null || editingSectionId.value !== null) {
      if (editingItemId.value !== item.id) openEdit(item.id)
    } else if (movingItemId.value !== null || movingSectionId.value !== null) {
      if (movingItemId.value !== item.id) openSort(item.id)
    }
  }

  function onSectionTitleClick(marker) {
    if (editingItemId.value !== null || editingSectionId.value !== null) {
      if (editingSectionId.value !== marker.id) openEditSection(marker.id)
    } else if (movingItemId.value !== null || movingSectionId.value !== null) {
      if (movingSectionId.value !== marker.id) openSortSection(marker.id)
    }
    // else: no active session — a bare click on the static title does nothing;
    // the user must open the overlay (long-press / dots) first.
  }

  function swapFlat(a, b) {
    const ia = list.value.indexOf(a)
    const ib = list.value.indexOf(b)
    list.value[ia] = b
    list.value[ib] = a
  }

  function moveItem(group, item, dir) {
    const idx = group.items.indexOf(item)
    const newIdx = idx + dir
    if (newIdx < 0 || newIdx >= group.items.length) return
    swapFlat(item, group.items[newIdx])
    renumberAndPersist()
  }

  function otherSections(item) {
    const currentGroup = groupedItems.value.find((g) => g.items.includes(item))
    return groupedItems.value.filter((g) => g.marker && g.marker !== currentGroup?.marker)
  }

  function moveItemToSection(item, targetMarker) {
    const idx = list.value.indexOf(item)
    list.value.splice(idx, 1)
    const markerIdx = list.value.indexOf(targetMarker)
    let insertAt = list.value.length
    for (let i = markerIdx + 1; i < list.value.length; i++) {
      if (list.value[i].name.startsWith('section:')) {
        insertAt = i
        break
      }
    }
    list.value.splice(insertAt, 0, item)
    renumberAndPersist()
    sectionPickerItemId.value = null
  }

  function moveSection(marker, dir) {
    const reorderable = reorderableSections()
    const idx = reorderable.findIndex((g) => g.marker === marker)
    if (idx === -1) return
    const newIdx = idx + dir
    if (newIdx < 0 || newIdx >= reorderable.length) return
    const reordered = reorderable.slice()
    ;[reordered[idx], reordered[newIdx]] = [reordered[newIdx], reordered[idx]]
    list.value = rebuildFlatWithReorderedSections(reordered)
    renumberAndPersist()
  }

  async function renumberAndPersist() {
    const jobs = []
    list.value.forEach((it, i) => {
      const newIndex = (i + 1) * 1_000_000
      if (it.index !== newIndex) {
        it.index = newIndex
        jobs.push(persistReorder(it, newIndex))
      }
    })
    await Promise.all(jobs)
  }

  const press = {
    kind: null,
    itemId: null,
    sectionId: null,
    startX: 0,
    startY: 0,
    moved: false,
    timer: null
  }

  function clearLongPress() {
    if (press.timer) {
      clearTimeout(press.timer)
      press.timer = null
    }
  }

  function dismissMenus(target) {
    if (target.closest('.session-bar')) return false
    if (onOutsideClick && onOutsideClick(target)) return true
    if (movingItemId.value && !target.closest(`[data-move-overlay="item:${movingItemId.value}"]`)) {
      // Clicking a different row or section header is handled by onRowClick /
      // onSectionTitleMouseDown (switches the session there instead of dismissing) —
      // only actually close here when the click is truly outside any row or section.
      if (!target.closest('[data-wrap]') && !target.closest('.section-header')) {
        movingItemId.value = null
        sectionPickerItemId.value = null
      }
      return true
    }
    if (
      movingSectionId.value &&
      !target.closest(`[data-move-overlay="section:${movingSectionId.value}"]`)
    ) {
      if (!target.closest('[data-wrap]') && !target.closest('.section-header')) {
        movingSectionId.value = null
      }
      return true
    }
    return false
  }

  function pressDown(x, y, target) {
    if (dismissMenus(target)) return
    if (target.closest(EXCLUDE_SEL)) return
    if (isDesktop.value) return

    const wrap = target.closest('[data-wrap]')
    const sectionHeader = !wrap ? target.closest('.section-header') : null
    if (!wrap && !sectionHeader) return

    press.startX = x
    press.startY = y
    press.moved = false
    clearLongPress()

    if (wrap) {
      press.kind = 'item'
      press.itemId = Number(wrap.getAttribute('data-wrap'))
    } else {
      const sectionWrap = sectionHeader.closest('[data-section-wrap]')
      if (!sectionWrap) return
      press.kind = 'section'
      press.sectionId = Number(sectionWrap.getAttribute('data-section-wrap'))
    }

    press.timer = setTimeout(() => {
      press.timer = null
      if (press.moved) return
      if (press.kind === 'item') movingItemId.value = press.itemId
      else movingSectionId.value = press.sectionId
    }, LONG_PRESS_MS)
  }

  function pressMove(x, y) {
    if (press.timer && !press.moved) {
      if (
        Math.abs(x - press.startX) > MOVE_CANCEL_PX ||
        Math.abs(y - press.startY) > MOVE_CANCEL_PX
      ) {
        press.moved = true
        clearLongPress()
      }
    }
  }

  function pressUp() {
    clearLongPress()
  }

  /* ---------- grip drag: reorder + move item across sections ---------- */
  const xdrag = {
    pending: false,
    started: false,
    kind: null,
    id: null,
    startX: 0,
    startY: 0,
    pointerOffsetY: 0,
    ghostLeft: 0,
    ghostEl: null,
    indicatorEl: null,
    sourceEl: null
  }

  function gripDown(x, y, gripEl) {
    const wrap = gripEl.closest('[data-wrap]')
    const sectionWrap = !wrap ? gripEl.closest('[data-section-wrap]') : null
    if (!wrap && !sectionWrap) return

    xdrag.pending = true
    xdrag.started = false
    xdrag.startX = x
    xdrag.startY = y

    if (wrap) {
      xdrag.kind = 'item'
      xdrag.id = Number(wrap.getAttribute('data-wrap'))
      xdrag.sourceEl = wrap
    } else {
      xdrag.kind = 'section'
      xdrag.id = Number(sectionWrap.getAttribute('data-section-wrap'))
      xdrag.sourceEl = sectionWrap
    }
  }

  function findItemById(id) {
    for (const it of list.value) {
      if (String(it.id) === String(id)) return it
    }
    return null
  }

  function startXDragVisuals(x, y) {
    xdrag.started = true
    const rect = xdrag.sourceEl.getBoundingClientRect()
    const label =
      xdrag.kind === 'item'
        ? findItemById(xdrag.id)?.name
        : findItemById(xdrag.id)?.name.replace('section:', '')

    const ghost = document.createElement('div')
    ghost.className =
      'fixed z-[9999] pointer-events-none bg-white border border-blue-600 shadow-lg rounded-md px-3 py-2 text-sm font-semibold text-gray-900 max-w-[240px] overflow-hidden text-ellipsis whitespace-nowrap'
    ghost.textContent = label
    ghost.style.width = Math.min(rect.width - 32, 240) + 'px'
    document.body.appendChild(ghost)
    xdrag.ghostEl = ghost
    xdrag.pointerOffsetY = y - rect.top
    xdrag.ghostLeft = rect.left + 16

    const indicator = document.createElement('div')
    indicator.className = 'h-[3px] bg-blue-600 rounded mx-4 my-1'
    xdrag.indicatorEl = indicator
    xdrag.sourceEl.parentNode.insertBefore(indicator, xdrag.sourceEl.nextSibling)
    xdrag.sourceEl.classList.add('opacity-30')
  }

  function positionIndicatorForItem(y) {
    const root = rootEl.value
    const wraps = Array.from(root.querySelectorAll('[data-wrap]')).filter(
      (w) => w !== xdrag.sourceEl
    )
    let best = null,
      bestDist = Infinity,
      before = true
    wraps.forEach((w) => {
      const r = w.getBoundingClientRect()
      const mid = r.top + r.height / 2
      const dist = Math.abs(y - mid)
      if (dist < bestDist) {
        bestDist = dist
        best = w
        before = y < mid
      }
    })
    if (best) {
      best.parentNode.insertBefore(xdrag.indicatorEl, before ? best : best.nextSibling)
      return
    }
    const lists = Array.from(root.querySelectorAll('[data-items-list]'))
    let bestList = null
    bestDist = Infinity
    lists.forEach((l) => {
      const r = l.getBoundingClientRect()
      const mid = r.top + r.height / 2
      const dist = Math.abs(y - mid)
      if (dist < bestDist) {
        bestDist = dist
        bestList = l
      }
    })
    if (bestList) bestList.appendChild(xdrag.indicatorEl)
  }

  function positionIndicatorForSection(y) {
    const root = rootEl.value
    const cards = Array.from(root.querySelectorAll('[data-section-wrap]')).filter(
      (c) => c !== xdrag.sourceEl
    )
    let best = null,
      bestDist = Infinity,
      before = true
    cards.forEach((c) => {
      const r = c.getBoundingClientRect()
      const mid = r.top + r.height / 2
      const dist = Math.abs(y - mid)
      if (dist < bestDist) {
        bestDist = dist
        best = c
        before = y < mid
      }
    })
    if (best) best.parentNode.insertBefore(xdrag.indicatorEl, before ? best : best.nextSibling)
  }

  function gripMove(x, y) {
    if (!xdrag.pending) return
    if (!xdrag.started) {
      if (Math.abs(x - xdrag.startX) < 4 && Math.abs(y - xdrag.startY) < 4) return
      startXDragVisuals(x, y)
    }
    xdrag.ghostEl.style.top = y - xdrag.pointerOffsetY + 'px'
    xdrag.ghostEl.style.left = xdrag.ghostLeft + 'px'
    if (xdrag.kind === 'item') positionIndicatorForItem(y)
    else positionIndicatorForSection(y)
  }

  function gripUp() {
    if (!xdrag.pending) return
    xdrag.pending = false
    if (!xdrag.started) return
    xdrag.started = false

    if (xdrag.ghostEl) {
      xdrag.ghostEl.remove()
      xdrag.ghostEl = null
    }
    xdrag.sourceEl.classList.remove('opacity-30')

    if (xdrag.kind === 'item') {
      const listEl = xdrag.indicatorEl.closest('[data-items-list]')
      let idx = 0
      if (listEl) {
        for (const child of listEl.children) {
          if (child === xdrag.indicatorEl) break
          if (child.hasAttribute && child.hasAttribute('data-wrap')) idx++
        }
      }
      xdrag.indicatorEl.remove()

      const item = findItemById(xdrag.id)
      if (item && listEl) {
        const flatIdx = list.value.indexOf(item)
        list.value.splice(flatIdx, 1)
        // find insertion anchor: the target items-list's marker id (or 'none')
        const targetMarkerId = listEl.getAttribute('data-items-list')
        let insertAt
        if (targetMarkerId === 'none') {
          insertAt = idx
        } else {
          const markerItem = list.value.find((it) => String(it.id) === String(targetMarkerId))
          insertAt = list.value.indexOf(markerItem) + 1 + idx
        }
        list.value.splice(insertAt, 0, item)
        renumberAndPersist()
      }
      // Keep the action overlay/menu open on the item in its new spot so the user
      // can keep acting on it (drag again, edit, etc.) without reopening the menu.
    } else {
      const root = rootEl.value
      const sectionWraps = Array.from(root.querySelectorAll('[data-section-wrap]')).filter(
        (w) => w !== xdrag.sourceEl
      )
      // compute index among the *other* section groups by DOM order relative to the drop indicator
      let targetPos = sectionWraps.length
      for (let i = 0; i < sectionWraps.length; i++) {
        if (
          xdrag.indicatorEl.compareDocumentPosition(sectionWraps[i]) &
            Node.DOCUMENT_POSITION_FOLLOWING &&
          !(
            xdrag.indicatorEl.compareDocumentPosition(sectionWraps[i]) &
            Node.DOCUMENT_POSITION_CONTAINED_BY
          )
        ) {
          targetPos = i
          break
        }
      }
      xdrag.indicatorEl.remove()

      const reorderable = reorderableSections()
      const srcIdx = reorderable.findIndex((g) => g.marker.id === xdrag.id)
      if (srcIdx > -1) {
        const reordered = reorderable.slice()
        const [moved] = reordered.splice(srcIdx, 1)
        const insertIdx = Math.min(targetPos, reordered.length)
        reordered.splice(insertIdx, 0, moved)
        list.value = rebuildFlatWithReorderedSections(reordered)
        renumberAndPersist()
      }
      // Keep the section's action overlay open in its new spot, same as items.
    }
  }

  function onMouseDown(e) {
    const grip = e.target.closest('.grip')
    if (grip) {
      gripDown(e.clientX, e.clientY, grip)
      return
    }
    pressDown(e.clientX, e.clientY, e.target)
  }
  function onMouseMove(e) {
    gripMove(e.clientX, e.clientY)
    pressMove(e.clientX, e.clientY)
  }
  function onMouseUp() {
    gripUp()
    pressUp()
  }
  function onTouchStart(e) {
    const t = e.touches[0]
    const grip = e.target.closest('.grip')
    if (grip) {
      gripDown(t.clientX, t.clientY, grip)
      return
    }
    pressDown(t.clientX, t.clientY, e.target)
  }
  function onTouchMove(e) {
    const t = e.touches[0]
    gripMove(t.clientX, t.clientY)
    pressMove(t.clientX, t.clientY)
  }
  function onTouchEnd() {
    gripUp()
    pressUp()
  }

  let boundEl = null

  onMounted(() => {
    const el = rootEl.value
    boundEl = el
    el.addEventListener('mousedown', onMouseDown)
    window.addEventListener('mousemove', onMouseMove)
    window.addEventListener('mouseup', onMouseUp)
    el.addEventListener('touchstart', onTouchStart, { passive: true })
    el.addEventListener('touchmove', onTouchMove, { passive: true })
    el.addEventListener('touchend', onTouchEnd)
  })

  onBeforeUnmount(() => {
    window.removeEventListener('mousemove', onMouseMove)
    window.removeEventListener('mouseup', onMouseUp)
    if (boundEl) {
      boundEl.removeEventListener('mousedown', onMouseDown)
      boundEl.removeEventListener('touchstart', onTouchStart)
      boundEl.removeEventListener('touchmove', onTouchMove)
      boundEl.removeEventListener('touchend', onTouchEnd)
    }
  })

  return {
    editingItemId,
    editingSectionId,
    movingItemId,
    movingSectionId,
    sectionPickerItemId,
    groupedItems,
    openEdit,
    openEditSection,
    closeEditSection,
    openSort,
    openSortSection,
    closeEdit,
    closeSession,
    setSessionMode,
    onRowClick,
    onSectionTitleClick,
    toggleItemOverlay,
    closeItemOverlay,
    toggleSectionOverlay,
    moveItem,
    moveSection,
    moveItemToSection,
    otherSections,
    isFirstSection,
    isLastSection,
    // Not part of the spec'd return list, but addItemToGroup() in TripChecklist.vue (a
    // domain function that intentionally stayed out of this composable) needs to persist
    // index renumbering after inserting a new item — exposed here so that logic isn't
    // duplicated outside the composable.
    renumberAndPersist
  }
}
