<template>
  <div
    class="relative"
    :class="{ 'pb-16': editingItemId || movingItemId || movingSectionId }"
    ref="rootEl"
  >
    <ListSkeleton v-if="!items" />

    <template v-else>
      <p
        v-if="!editingItemId && !movingItemId && !movingSectionId"
        class="text-center text-xs text-gray-400 px-6 py-2 md:hidden"
      >
        Trykk og hold en vare eller seksjon for å åpne menyen
      </p>
      <p
        v-if="!editingItemId && !movingItemId && !movingSectionId"
        class="text-center text-xs text-gray-400 px-6 py-2 max-md:hidden"
      >
        Klikk <DotsVerticalIcon class="inline w-3 h-3 align-middle" /> for å åpne menyen
      </p>
      <div
        v-if="editingItemId || movingItemId || movingSectionId"
        class="session-bar fixed bottom-0 inset-x-0 z-40 px-4 py-2.5 bg-blue-50 border-t border-blue-200 shadow-[0_-4px_12px_rgba(0,0,0,0.08)]"
      >
        <p class="text-center text-[11px] text-blue-700 font-medium mb-2">
          {{
            editingItemId
              ? 'Du redigerer — trykk en annen vare for å fortsette der, eller avslutt når du er ferdig.'
              : 'Du sorterer — trykk en annen vare eller seksjon for å flytte den i stedet, eller dra i ⠿.'
          }}
        </p>
        <div class="flex items-center justify-center gap-3">
          <div class="flex items-center bg-white border border-blue-200 rounded-full p-0.5 gap-0.5">
            <button
              class="flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold disabled:opacity-40 disabled:cursor-not-allowed"
              :class="editingItemId ? 'bg-blue-600 text-white' : 'text-blue-700 hover:bg-blue-50'"
              :disabled="movingSectionId !== null"
              @click="setSessionMode('edit')"
            >
              <EditIcon class="w-3.5 h-3.5" />
              Redigering
            </button>
            <button
              class="flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold"
              :class="
                movingItemId || movingSectionId
                  ? 'bg-blue-600 text-white'
                  : 'text-blue-700 hover:bg-blue-50'
              "
              @click="setSessionMode('sort')"
            >
              <HamburgerMenuIcon class="w-3.5 h-3.5" />
              Sortering
            </button>
          </div>
          <button
            class="text-xs font-bold text-blue-700 hover:text-blue-900"
            @click="closeSession()"
          >
            Ferdig
          </button>
        </div>
      </div>

      <div v-if="items.length === 0" class="text-left w-full px-5 py-2">
        <p class="text-md">
          Du har ingenting i pakkelisten din enda! Vil du kopiere listen din fra sist?
        </p>
        <SecondaryButton @click="copyItemsFromOtherTrip()" class="me-2 mt-2"
          >📋 kopier fra sist</SecondaryButton
        >
      </div>

      <div
        v-for="group in groupedItems"
        :key="group.marker?.id ?? 'ungrouped'"
        class="relative border-b-4 border-gray-100"
        :data-section-wrap="group.marker ? group.marker.id : undefined"
      >
        <!-- section header -->
        <div
          v-if="group.marker"
          class="section-header px-4 pt-4 pb-2"
          :class="{ 'opacity-30': movingSectionId === group.marker.id }"
        >
          <div class="flex items-center gap-2">
            <input
              class="flex-1 min-w-0 text-xl font-bold text-gray-900 bg-transparent hover:bg-gray-50 focus:bg-gray-50 outline-none rounded-md px-1 py-0.5"
              :value="group.marker.name.replace('section:', '')"
              @mousedown="onSectionTitleMouseDown($event, group.marker)"
              @keydown.enter="(e) => renameSection(group.marker, e.target.value)"
              @blur="(e) => renameSection(group.marker, e.target.value)"
            />
            <button
              v-if="isDesktop"
              class="p-1.5 rounded-md text-gray-400 hover:bg-gray-100 hover:text-gray-700 flex-shrink-0"
              @click.stop="toggleSectionOverlay(group.marker.id)"
            >
              <DotsVerticalIcon />
            </button>
          </div>
          <div class="flex justify-between text-xs font-semibold text-gray-500 mt-2 mb-1">
            <span>{{ packedCount(group) }}/{{ group.items.length }} pakket</span>
          </div>
          <div class="h-1.5 rounded-full bg-gray-100 overflow-hidden">
            <div
              class="h-full rounded-full bg-green-600 transition-all"
              :style="{ width: sectionPercent(group) + '%' }"
            ></div>
          </div>
        </div>

        <!-- items -->
        <div
          :data-items-list="group.marker?.id ?? 'none'"
          :class="{ 'opacity-30': group.marker && movingSectionId === group.marker.id }"
        >
          <div
            v-for="item in group.items"
            :key="item.id"
            class="relative border-t border-gray-100 row-wrap"
            :data-wrap="item.id"
          >
            <div
              v-if="editingItemId === item.id"
              class="flex items-start gap-2 px-4 py-2.5 bg-gray-50"
            >
              <div class="flex-1 min-w-0 flex flex-col gap-1.5">
                <div class="flex items-center gap-2">
                  <input
                    class="flex-1 min-w-0 text-sm font-medium text-gray-900 bg-transparent hover:bg-white focus:bg-white outline-none rounded-md px-1 py-0.5"
                    :value="item.name"
                    :ref="(el) => el && editingItemId === item.id && focusSoon(el)"
                    @keydown.enter="(e) => e.target.blur()"
                    @blur="(e) => editItemName(item, e.target.value)"
                  />
                  <CounterInput
                    :value="item.quantity"
                    :editable="true"
                    @update:value="($event) => updateItem(item, 'quantity', $event)"
                  />
                  <button
                    class="p-1.5 rounded-md text-gray-400 hover:bg-gray-100 hover:text-gray-700 flex-shrink-0"
                    @click="closeEdit()"
                  >
                    <CheckIcon class="h-4 w-4" />
                  </button>
                </div>
                <div class="relative w-fit px-1" :data-target-picker-owner="item.id">
                  <button
                    class="flex items-center gap-1 text-xs font-semibold text-blue-600 border-b border-dashed border-blue-300 py-0.5 hover:border-blue-500"
                    @click.stop="toggleTargetPicker(item.id)"
                  >
                    <span>{{ targetOf(item)?.name ?? '— ingen —' }}</span>
                    <span class="text-blue-400">▾</span>
                  </button>
                  <div
                    v-if="targetPickerItemId === item.id"
                    class="absolute left-0 top-7 z-50 bg-white border-2 border-gray-300 rounded-xl shadow-2xl p-1 min-w-[190px] flex flex-col gap-0.5 max-h-[50vh] overflow-y-auto"
                  >
                    <button
                      class="px-2.5 py-2 rounded-md hover:bg-gray-100 w-full text-left text-sm text-gray-500"
                      @click="setSupplyTarget(item, null)"
                    >
                      — ingen —
                    </button>
                    <button
                      v-for="t in supplyTargets"
                      :key="t.id"
                      class="px-2.5 py-2 rounded-md hover:bg-gray-100 w-full text-left text-sm text-gray-900"
                      @click="setSupplyTarget(item, t.id)"
                    >
                      {{ t.name }}
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <div
              v-else
              class="flex items-center gap-2.5 px-4 py-2.5"
              :class="[
                { 'opacity-35': movingItemId === item.id },
                editingItemId !== null || movingItemId !== null
                  ? 'cursor-pointer hover:bg-gray-50'
                  : ''
              ]"
              @click="onRowClick(item)"
            >
              <div class="flex-1 min-w-0">
                <div
                  class="text-sm font-medium truncate"
                  :class="item.packed ? 'text-gray-400 line-through' : 'text-gray-900'"
                >
                  <span v-if="item.quantity > 1" class="text-gray-500 font-semibold"
                    >×{{ item.quantity }}&nbsp;</span
                  >{{ item.name }}
                </div>
                <div v-if="targetOf(item)" class="text-xs font-semibold text-blue-600 mt-0.5">
                  🎯 {{ targetOf(item).name }}
                </div>
              </div>
              <div class="flex items-center gap-1.5 flex-shrink-0" @click.stop>
                <CheckBox v-model="item.packed" @input="updateItem(item, 'packed', !item.packed)" />
                <button
                  v-if="isDesktop && editingItemId"
                  class="p-1.5 rounded-md text-gray-400 hover:bg-gray-100 hover:text-gray-700 flex-shrink-0"
                  @click.stop="openEdit(item.id)"
                >
                  <EditIcon />
                </button>
                <button
                  v-else-if="isDesktop"
                  class="p-1.5 rounded-md text-gray-400 hover:bg-gray-100 hover:text-gray-700 flex-shrink-0"
                  @click.stop="toggleItemOverlay(item.id)"
                >
                  <DotsVerticalIcon />
                </button>
              </div>
            </div>

            <div
              v-if="movingItemId === item.id"
              class="move-overlay absolute inset-0 flex items-center justify-center bg-gray-900/45 rounded-md z-50"
              :data-move-overlay="'item:' + item.id"
              @click.self="closeItemOverlay()"
            >
              <div
                v-if="sectionPickerItemId === item.id"
                class="bg-white border-2 border-gray-300 rounded-2xl shadow-2xl p-2 min-w-[200px] max-w-[260px]"
              >
                <div class="px-2 pt-1 pb-1 text-xs font-semibold text-gray-500">
                  Flytt til seksjon
                </div>
                <button
                  v-for="g in otherSections(item)"
                  :key="g.marker.id"
                  class="flex items-center px-2.5 py-2 rounded-md hover:bg-gray-100 w-full text-left text-sm text-gray-900"
                  @click="moveItemToSection(item, g.marker)"
                >
                  {{ g.marker.name.replace('section:', '') }}
                </button>
                <button
                  class="px-2.5 py-2 rounded-md hover:bg-gray-100 w-full text-left text-sm text-gray-500"
                  @click="sectionPickerItemId = null"
                >
                  Avbryt
                </button>
              </div>
              <ActionStrip
                v-else
                :is-first="group.items[0]?.id === item.id"
                :is-last="group.items[group.items.length - 1]?.id === item.id"
                :show-edit="true"
                :label="item.name"
                @up="moveItem(group, item, -1)"
                @down="moveItem(group, item, 1)"
                @edit="openEdit(item.id)"
                @delete="removeItem(item)"
                @move-to-section="sectionPickerItemId = item.id"
              />
            </div>
          </div>

          <template v-if="group.marker">
            <div v-if="addingItemSectionId === group.marker.id">
              <div
                class="flex items-center gap-2 px-4 py-2.5 border-t border-dashed border-gray-200"
              >
                <input
                  class="flex-1 min-w-0 text-sm font-medium text-gray-900 bg-transparent hover:bg-gray-50 focus:bg-gray-50 outline-none rounded-md px-1 py-0.5"
                  placeholder="Navn på vare"
                  v-model="newItemName"
                  :ref="(el) => el && addingItemSectionId === group.marker.id && focusSoon(el)"
                  @keydown.enter="addItemToGroup(group, newItemName)"
                  @keydown.esc="addingItemSectionId = null"
                />
                <button
                  class="p-1.5 rounded-md text-gray-400 hover:bg-gray-100 hover:text-gray-700 flex-shrink-0"
                  @click="addItemToGroup(group, newItemName)"
                >
                  <PlusIcon class="h-4 w-4" />
                </button>
              </div>
              <p v-if="errorMsg" class="text-xs text-red-600 px-4 pb-1.5">{{ errorMsg }}</p>
            </div>
            <button
              v-else
              class="w-full text-left px-4 py-2.5 text-sm font-semibold text-gray-500 hover:bg-gray-50 hover:text-blue-600 border-t border-dashed border-gray-200"
              @click="startAddItem(group)"
            >
              + Legg til vare
            </button>
          </template>
        </div>

        <div
          v-if="group.marker && movingSectionId === group.marker.id"
          class="move-overlay absolute inset-0 flex items-center justify-center bg-gray-900/45 rounded-md z-50"
          :data-move-overlay="'section:' + group.marker.id"
          @click.self="movingSectionId = null"
        >
          <ActionStrip
            :is-first="isFirstSection(group.marker)"
            :is-last="isLastSection(group.marker)"
            :show-edit="false"
            :label="group.marker.name.replace('section:', '')"
            @up="moveSection(group.marker, -1)"
            @down="moveSection(group.marker, 1)"
            @delete="deleteSection(group.marker)"
          />
        </div>
      </div>

      <div class="px-4 py-3 flex flex-col gap-2">
        <div
          v-if="addingSection"
          class="flex items-center gap-2 px-2 py-1 border border-dashed border-gray-300 rounded-lg mt-2"
        >
          <input
            class="flex-1 min-w-0 text-sm font-medium text-gray-900 bg-transparent hover:bg-gray-50 focus:bg-gray-50 outline-none rounded-md px-1 py-1.5"
            placeholder="Navn på seksjon"
            v-model="newSectionName"
            :ref="(el) => el && addingSection && focusSoon(el)"
            @keydown.enter="confirmAddSection()"
            @keydown.esc="addingSection = false"
          />
          <button
            class="p-1.5 rounded-md text-gray-400 hover:bg-gray-100 hover:text-gray-700 flex-shrink-0"
            @click="confirmAddSection()"
          >
            <PlusIcon class="h-4 w-4" />
          </button>
        </div>
        <button
          v-else
          class="w-full text-center px-4 py-2.5 text-sm font-semibold text-gray-500 hover:bg-gray-50 hover:text-blue-600 border border-dashed border-gray-300 rounded-lg mt-2"
          @click="startAddSection()"
        >
          + Ny seksjon
        </button>
      </div>
    </template>
  </div>
</template>

<script setup>
import ListSkeleton from '@/components/ListSkeleton.vue'
import DraggableItemIcon from '@/components/icons/DraggableItemIcon.vue'
import PlusIcon from '@/components/icons/PlusIcon.vue'
import DotsVerticalIcon from '@/components/icons/DotsVerticalIcon.vue'
import HamburgerMenuIcon from '@/components/icons/HamburgerMenuIcon.vue'
import CheckIcon from '@/components/icons/CheckIcon.vue'
import { computed, h, nextTick, onBeforeUnmount, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import SecondaryButton from './ui/SecondaryButton.vue'
import CheckBox from './ui/CheckBox.vue'
import EditIcon from './icons/EditIcon.vue'
import TrashIcon from './icons/TrashIcon.vue'
import ArrowUpIcon from './icons/ArrowUpIcon.vue'
import ArrowRightIcon from './icons/ArrowRightIcon.vue'
import ArrowDownIcon from './icons/ArrowDownIcon.vue'
import CounterInput from './ui/CounterInput.vue'

/* ---------- small local action-menu components (icon + subtle caption, shared style) ---------- */
function menuButtonProps() {
  return {
    isFirst: { type: Boolean, default: false },
    isLast: { type: Boolean, default: false },
    showEdit: { type: Boolean, default: false },
    label: { type: String, default: '' }
  }
}

const ActionStrip = {
  props: menuButtonProps(),
  emits: ['up', 'down', 'edit', 'delete', 'move-to-section'],
  render() {
    const btn = (icon, label, onClick, opts = {}) =>
      h(
        'button',
        {
          class: [
            'flex flex-col items-center justify-center gap-0.5 w-14 py-2 rounded-lg hover:bg-gray-100 disabled:opacity-30 disabled:hover:bg-transparent',
            opts.danger ? 'text-red-600' : 'text-gray-700',
            opts.grip ? 'cursor-grab grip' : '',
            // Dragging works poorly on touch anyway, so hide it on narrow screens to save space
            // — it stays available from sm (~tablet/desktop) up, where mouse dragging is natural.
            opts.hideOnMobile ? 'hidden sm:flex' : ''
          ],
          disabled: opts.disabled,
          onClick
        },
        [h(icon, { class: 'w-5 h-5' }), h('span', { class: 'text-[10px] font-semibold text-gray-500' }, label)]
      )
    const children = [btn(DraggableItemIcon, 'Dra', undefined, { grip: true, hideOnMobile: true })]
    children.push(btn(ArrowUpIcon, 'Opp', () => this.$emit('up'), { disabled: this.isFirst }))
    children.push(btn(ArrowDownIcon, 'Ned', () => this.$emit('down'), { disabled: this.isLast }))
    if (this.showEdit) {
      children.push(btn(ArrowRightIcon, 'Flytt til', () => this.$emit('move-to-section')))
      children.push(btn(EditIcon, 'Rediger', () => this.$emit('edit')))
    }
    children.push(btn(TrashIcon, 'Slett', () => this.$emit('delete'), { danger: true }))
    const buttonRow = h('div', { class: 'flex gap-0.5' }, children)
    const nameLabel = this.label
      ? h(
          'div',
          {
            class:
              'text-center text-[11px] font-semibold text-gray-700 truncate max-w-[240px] px-2 pb-1'
          },
          this.label
        )
      : null
    return h(
      'div',
      { class: 'bg-white rounded-2xl shadow-xl p-1.5 flex flex-col items-center' },
      nameLabel ? [nameLabel, buttonRow] : [buttonRow]
    )
  }
}

const items = ref(null)
const supplyTargets = ref(null)
const newItemName = ref('')
const newSectionName = ref('')
const errorMsg = ref(null)
const rootEl = ref(null)

const editingItemId = ref(null)
const movingItemId = ref(null)
const movingSectionId = ref(null)
const sectionPickerItemId = ref(null)
const targetPickerItemId = ref(null)
const addingSection = ref(false)
const addingItemSectionId = ref(null)

const isDesktop = ref(window.matchMedia('(min-width: 768px)').matches)
const desktopMql = window.matchMedia('(min-width: 768px)')
function onMqlChange(e) {
  isDesktop.value = e.matches
}

const params = useRoute().params

// Focusing an input right as it's mounted can lose to the browser resetting focus
// to <body> when the element it replaces (e.g. an "add" button) is removed in the
// same patch, so wait for Vue's DOM update to fully settle first.
function focusSoon(el) {
  nextTick(() => {
    requestAnimationFrame(() => el.focus())
  })
}

const groupedItems = computed(() => {
  const groups = []
  let current = { marker: null, items: [] }
  for (const it of items.value || []) {
    if (it.name.startsWith('section:')) {
      groups.push(current)
      current = { marker: it, items: [] }
    } else {
      current.items.push(it)
    }
  }
  groups.push(current)
  return groups
})

function targetOf(item) {
  return supplyTargets.value?.find((t) => t.id === item.supply_target_id) || null
}

function packedCount(group) {
  return group.items.filter((i) => i.packed).length
}
function sectionPercent(group) {
  if (!group.items.length) return 0
  return Math.round((packedCount(group) / group.items.length) * 100)
}
function isFirstSection(marker) {
  const groups = groupedItems.value.filter((g) => g.marker)
  return groups[0]?.marker.id === marker.id
}
function isLastSection(marker) {
  const groups = groupedItems.value.filter((g) => g.marker)
  return groups[groups.length - 1]?.marker.id === marker.id
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
  targetPickerItemId.value = null
  editingItemId.value = id
}

function openSort(id) {
  editingItemId.value = null
  targetPickerItemId.value = null
  movingItemId.value = id
  movingSectionId.value = null
  sectionPickerItemId.value = null
}

function openSortSection(id) {
  editingItemId.value = null
  targetPickerItemId.value = null
  movingItemId.value = null
  sectionPickerItemId.value = null
  movingSectionId.value = id
}

function closeEdit() {
  editingItemId.value = null
  targetPickerItemId.value = null
}

function closeSession() {
  editingItemId.value = null
  movingItemId.value = null
  movingSectionId.value = null
  sectionPickerItemId.value = null
  targetPickerItemId.value = null
}

function setSessionMode(mode) {
  const currentId = editingItemId.value ?? movingItemId.value
  if (currentId === null) return
  if (mode === 'edit') openEdit(currentId)
  else openSort(currentId)
}

function onRowClick(item) {
  if (editingItemId.value !== null) {
    if (editingItemId.value !== item.id) openEdit(item.id)
  } else if (movingItemId.value !== null || movingSectionId.value !== null) {
    if (movingItemId.value !== item.id) openSort(item.id)
  }
}

function onSectionTitleMouseDown(e, marker) {
  if (
    editingItemId.value === null &&
    (movingItemId.value !== null || movingSectionId.value !== null)
  ) {
    if (movingSectionId.value !== marker.id) {
      e.preventDefault()
      openSortSection(marker.id)
    }
  }
}

function toggleTargetPicker(id) {
  targetPickerItemId.value = targetPickerItemId.value === id ? null : id
}

function setSupplyTarget(item, targetId) {
  updateItem(item, 'supply_target_id', targetId)
  targetPickerItemId.value = null
}

function swapFlat(a, b) {
  const ia = items.value.indexOf(a)
  const ib = items.value.indexOf(b)
  items.value[ia] = b
  items.value[ib] = a
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
  const idx = items.value.indexOf(item)
  items.value.splice(idx, 1)
  const markerIdx = items.value.indexOf(targetMarker)
  let insertAt = items.value.length
  for (let i = markerIdx + 1; i < items.value.length; i++) {
    if (items.value[i].name.startsWith('section:')) {
      insertAt = i
      break
    }
  }
  items.value.splice(insertAt, 0, item)
  renumberAndPersist()
  sectionPickerItemId.value = null
}

function moveSection(marker, dir) {
  const groups = groupedItems.value
  const idx = groups.findIndex((g) => g.marker === marker)
  const newIdx = idx + dir
  if (newIdx < 0 || newIdx >= groups.length) return
  if (!groups[newIdx].marker) return
  const reordered = groups.slice()
  ;[reordered[idx], reordered[newIdx]] = [reordered[newIdx], reordered[idx]]
  const flat = []
  for (const g of reordered) {
    if (g.marker) flat.push(g.marker)
    flat.push(...g.items)
  }
  items.value = flat
  renumberAndPersist()
}

async function renumberAndPersist() {
  const jobs = []
  items.value.forEach((it, i) => {
    const newIndex = (i + 1) * 1_000_000
    if (it.index !== newIndex) {
      it.index = newIndex
      jobs.push(updateItem(it, 'index', newIndex))
    }
  })
  await Promise.all(jobs)
}

function startAddItem(group) {
  addingItemSectionId.value = group.marker.id
  newItemName.value = ''
  errorMsg.value = null
}

async function addItemToGroup(group, itemName) {
  itemName = itemName.trim()
  if (itemName === '') {
    errorMsg.value = 'Kan ikke legge til ingenting!'
    return
  }
  const matchingElement = items.value.find(
    (i) =>
      i.name.localeCompare(itemName, undefined, {
        usage: 'search',
        sensitivity: 'base'
      }) == 0
  )
  if (matchingElement) {
    errorMsg.value = 'Dette er allerede i listen!'
    return
  }
  errorMsg.value = null
  const itemPosition = (items.value.slice(-1)[0]?.index || 0) + 1_000_000
  const response = await fetch(`/api/participant/${params.listId}/items`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name: itemName, index: itemPosition })
  })
  const item = await response.json()
  item._status = { editing: false }

  const insertAfter = group.items.length ? group.items[group.items.length - 1] : group.marker
  if (insertAfter) {
    const pos = items.value.indexOf(insertAfter)
    items.value.splice(pos + 1, 0, item)
  } else {
    items.value.unshift(item)
  }
  await renumberAndPersist()
  newItemName.value = ''
  // Keep the input open so the user can add several items in a row without touching the mouse.
}

function startAddSection() {
  addingSection.value = true
  newSectionName.value = items.value.length === 0 ? 'Pakkeliste' : ''
}

async function confirmAddSection() {
  const name = newSectionName.value.trim()
  if (!name) return
  const itemPosition = (items.value.slice(-1)[0]?.index || 0) + 1_000_000
  const response = await fetch(`/api/participant/${params.listId}/items`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name: `section:${name}`, index: itemPosition })
  })
  const item = await response.json()
  item._status = { editing: false }
  items.value.push(item)
  addingSection.value = false
}

async function removeItem(item) {
  const response = await fetch(`/api/participant/${params.listId}/items/${item.id}`, {
    method: 'DELETE',
    headers: { 'Content-Type': 'application/json' }
  })
  if (response.ok) items.value = items.value.filter((i) => i.id != item.id)
  movingItemId.value = null
  sectionPickerItemId.value = null
}

async function deleteSection(marker) {
  await removeItem(marker)
  movingSectionId.value = null
}

function editItemName(item, newName) {
  updateItem(item, 'name', newName)
}
function renameSection(marker, newTitle) {
  updateItem(marker, 'name', `section:${newTitle.trim() || marker.name.replace('section:', '')}`)
}

async function updateItem(item, attr, val) {
  // The backend replaces the whole row on every PUT (no partial updates), so the request
  // body is built from the current local item. Apply the change locally *before* awaiting
  // the request: otherwise, firing a second change (e.g. quantity) while the first one
  // (e.g. name) is still in flight would build its payload from a stale snapshot and
  // silently revert whatever the first change touched once both responses land.
  item[attr] = val
  try {
    const response = await fetch(`/api/participant/${params.listId}/items/${item.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...item, [attr]: val })
    })
    const savedItem = await response.json()
    item.index = savedItem.index
    item.name = savedItem.name
    item.supply_target_id = savedItem.supply_target_id
    item.quantity = savedItem.quantity
    item.packed = savedItem.packed
  } catch (err) {
    return err
  }
}

async function copyItemsFromOtherTrip() {
  const response = await fetch(`/api/trip/${params.tripId}/participant/${params.listId}/autofill`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: {}
  })
  if (response.ok) {
    const itemList = await response.json()
    items.value = itemList
      .map((item) => ({ ...item, _status: { editing: false } }))
      .sort((a, b) => a.index - b.index)
  }
}

/* ---------- long-press (mobile) opens the same menu as the desktop ⋮ ---------- */
const EXCLUDE_SEL = 'select, input, button, .move-overlay, .grip'
const LONG_PRESS_MS = 480
const MOVE_CANCEL_PX = 10

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
  if (
    targetPickerItemId.value &&
    !target.closest(`[data-target-picker-owner="${targetPickerItemId.value}"]`)
  ) {
    targetPickerItemId.value = null
    return true
  }
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
  for (const it of items.value) {
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
  const wraps = Array.from(root.querySelectorAll('[data-wrap]')).filter((w) => w !== xdrag.sourceEl)
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
      const flatIdx = items.value.indexOf(item)
      items.value.splice(flatIdx, 1)
      // find insertion anchor: the target items-list's marker id (or 'none')
      const targetMarkerId = listEl.getAttribute('data-items-list')
      let insertAt
      if (targetMarkerId === 'none') {
        insertAt = idx
      } else {
        const markerItem = items.value.find((it) => String(it.id) === String(targetMarkerId))
        insertAt = items.value.indexOf(markerItem) + 1 + idx
      }
      items.value.splice(insertAt, 0, item)
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

    const groups = groupedItems.value
    const namedGroups = groups.filter((g) => g.marker)
    const srcGroupIdx = namedGroups.findIndex((g) => g.marker.id === xdrag.id)
    if (srcGroupIdx > -1) {
      const reordered = namedGroups.slice()
      const [moved] = reordered.splice(srcGroupIdx, 1)
      const insertIdx = Math.min(targetPos, reordered.length)
      reordered.splice(insertIdx, 0, moved)
      const leading = groups[0].marker ? { marker: null, items: [] } : groups[0]
      const flat = []
      if (!leading.marker) flat.push(...leading.items)
      for (const g of reordered) {
        flat.push(g.marker, ...g.items)
      }
      items.value = flat
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

onMounted(async () => {
  desktopMql.addEventListener('change', onMqlChange)
  const el = rootEl.value
  el.addEventListener('mousedown', onMouseDown)
  window.addEventListener('mousemove', onMouseMove)
  window.addEventListener('mouseup', onMouseUp)
  el.addEventListener('touchstart', onTouchStart, { passive: true })
  el.addEventListener('touchmove', onTouchMove, { passive: true })
  el.addEventListener('touchend', onTouchEnd)

  try {
    const response = await fetch(`/api/trip/${params.tripId}/participant/${params.listId}/items`)
    const itemList = await response.json()
    items.value = itemList
      .map((item) => ({ ...item, _status: { editing: false } }))
      .sort((a, b) => a.index - b.index)
    const supplyResponse = await fetch(`/api/trip/${params.tripId}/supply-targets`)
    supplyTargets.value = await supplyResponse.json()
  } catch (err) {
    return err
  }
})

onBeforeUnmount(() => {
  desktopMql.removeEventListener('change', onMqlChange)
  window.removeEventListener('mousemove', onMouseMove)
  window.removeEventListener('mouseup', onMouseUp)
})
</script>
