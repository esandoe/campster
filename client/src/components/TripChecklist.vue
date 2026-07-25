<template>
  <div
    class="relative"
    :class="{ 'pb-16': editingItemId || editingSectionId || movingItemId || movingSectionId }"
    ref="rootEl"
  >
    <ListSkeleton v-if="!items" />

    <template v-else>
      <p
        v-if="!editingItemId && !editingSectionId && !movingItemId && !movingSectionId"
        class="text-center text-xs text-gray-400 px-6 py-2 md:hidden"
      >
        Trykk og hold en vare eller seksjon for å åpne menyen
      </p>
      <p
        v-if="!editingItemId && !editingSectionId && !movingItemId && !movingSectionId"
        class="text-center text-xs text-gray-400 px-6 py-2 max-md:hidden"
      >
        Klikk <DotsVerticalIcon class="inline w-3 h-3 align-middle" /> for å åpne menyen
      </p>
      <div
        v-if="editingItemId || editingSectionId || movingItemId || movingSectionId"
        class="session-bar fixed bottom-0 inset-x-0 z-40 px-4 py-2.5 bg-blue-50 border-t border-blue-200 shadow-[0_-4px_12px_rgba(0,0,0,0.08)]"
      >
        <p class="text-center text-[11px] text-blue-700 font-medium mb-2">
          {{
            editingItemId || editingSectionId
              ? 'Du redigerer — trykk en annen vare for å fortsette der, eller avslutt når du er ferdig.'
              : 'Du sorterer — trykk en annen vare eller seksjon for å flytte den i stedet, eller dra i ⠿.'
          }}
        </p>
        <div class="flex items-center justify-center gap-3">
          <div class="flex items-center bg-white border border-blue-200 rounded-full p-0.5 gap-0.5">
            <button
              class="flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold disabled:opacity-40 disabled:cursor-not-allowed"
              :class="
                editingItemId || editingSectionId
                  ? 'bg-blue-600 text-white'
                  : 'text-blue-700 hover:bg-blue-50'
              "
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

      <template v-for="group in groupedItems" :key="group.marker?.id ?? 'ungrouped'">
        <!-- grouped sections render inside a box -->
        <SectionBox v-if="group.marker" class="relative mb-3" :data-section-wrap="group.marker.id">
          <template #header>
            <div
              class="section-header"
              :class="{ 'opacity-30': movingSectionId === group.marker.id }"
            >
              <div class="flex items-center gap-2">
                <input
                  v-if="editingSectionId === group.marker.id"
                  class="flex-1 min-w-0 text-xl font-bold text-gray-900 bg-transparent hover:bg-white focus:bg-white outline-none rounded-md px-1 py-0.5 border border-gray-200"
                  :value="group.marker.name.replace('section:', '')"
                  :ref="(el) => el && (editSectionNameEl = el)"
                  @keydown.enter="(e) => e.target.blur()"
                  @blur="(e) => renameSection(group.marker, e.target.value)"
                />
                <div
                  v-else
                  class="flex-1 min-w-0 text-xl font-bold text-gray-900 truncate rounded-md px-1 py-0.5"
                  :class="[
                    { 'opacity-30': movingSectionId === group.marker.id },
                    editingItemId !== null ||
                    editingSectionId !== null ||
                    movingItemId !== null ||
                    movingSectionId !== null
                      ? 'cursor-pointer hover:bg-gray-50'
                      : ''
                  ]"
                  @click="onSectionTitleClick(group.marker)"
                >
                  {{ group.marker.name.replace('section:', '') }}
                </div>
                <button
                  v-if="editingSectionId === group.marker.id"
                  class="p-1.5 rounded-md text-gray-400 hover:bg-gray-100 hover:text-gray-700 flex-shrink-0"
                  @click="closeEditSection()"
                >
                  <CheckIcon class="h-4 w-4" />
                </button>
                <button
                  v-else-if="isDesktop && (editingItemId || editingSectionId)"
                  class="p-1.5 rounded-md text-gray-400 hover:bg-gray-100 hover:text-gray-700 flex-shrink-0"
                  @click.stop="openEditSection(group.marker.id)"
                >
                  <EditIcon />
                </button>
                <button
                  v-else-if="isDesktop"
                  class="p-1.5 rounded-md text-gray-400 hover:bg-gray-100 hover:text-gray-700 flex-shrink-0"
                  @click.stop="toggleSectionOverlay(group.marker.id)"
                >
                  <DotsVerticalIcon />
                </button>
              </div>
              <div class="flex justify-between text-xs font-semibold text-gray-500 mt-2 mb-1">
                <span>{{ packedCount(group) }}/{{ group.items.length }} pakket</span>
              </div>
              <CompactProgressBar :percent="sectionPercent(group)" variant="green" />
            </div>
          </template>

          <div
            :data-items-list="group.marker.id"
            :class="{ 'opacity-30': movingSectionId === group.marker.id }"
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
                      :ref="(el) => el && (editItemNameEl = el)"
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
                    🎯 {{ targetOf(item).name
                    }}<span v-if="targetOf(item).unit" class="text-gray-400 font-normal">
                      · {{ targetOf(item).unit }}</span
                    >
                  </div>
                </div>
                <div class="flex items-center gap-1.5 flex-shrink-0" @click.stop>
                  <CheckBox
                    v-model="item.packed"
                    @input="updateItem(item, 'packed', !item.packed)"
                  />
                  <button
                    v-if="isDesktop && (editingItemId || editingSectionId)"
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
                    :ref="(el) => el && (addItemNameEl = el)"
                    @keydown.enter="addItemToGroup(group, newItemName)"
                    @keydown.esc="addingItemSectionId = null"
                  />
                  <button
                    class="p-1.5 rounded-md text-blue-600 hover:bg-blue-50 flex-shrink-0"
                    @click="addItemToGroup(group, newItemName)"
                  >
                    <PlusIcon class="h-4 w-4" />
                  </button>
                  <div class="w-px self-stretch bg-gray-200 ml-1"></div>
                  <button
                    class="p-1.5 pl-2.5 rounded-md border-0 shadow-none bg-transparent text-gray-400 hover:bg-gray-100 hover:text-gray-700 focus:outline-none flex-shrink-0"
                    @click="addingItemSectionId = null"
                  >
                    <CloseIcon class="h-4 w-4" />
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

          <template #overlay>
            <div
              v-if="group.marker && movingSectionId === group.marker.id"
              class="move-overlay absolute inset-0 flex items-center justify-center bg-gray-900/45 rounded-md z-50"
              :data-move-overlay="'section:' + group.marker.id"
              @click.self="movingSectionId = null"
            >
              <ActionStrip
                :is-first="isFirstSection(group.marker)"
                :is-last="isLastSection(group.marker)"
                :show-edit="true"
                :show-move-to="false"
                :label="group.marker.name.replace('section:', '')"
                @up="moveSection(group.marker, -1)"
                @down="moveSection(group.marker, 1)"
                @edit="openEditSection(group.marker.id)"
                @delete="deleteSection(group.marker)"
              />
            </div>
          </template>
        </SectionBox>

        <!-- ungrouped items render bare (no box) -->
        <div v-else class="relative mb-3">
          <div :data-items-list="'none'">
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
                      :ref="(el) => el && (editItemNameEl = el)"
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
                    🎯 {{ targetOf(item).name
                    }}<span v-if="targetOf(item).unit" class="text-gray-400 font-normal">
                      · {{ targetOf(item).unit }}</span
                    >
                  </div>
                </div>
                <div class="flex items-center gap-1.5 flex-shrink-0" @click.stop>
                  <CheckBox
                    v-model="item.packed"
                    @input="updateItem(item, 'packed', !item.packed)"
                  />
                  <button
                    v-if="isDesktop && (editingItemId || editingSectionId)"
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
          </div>
        </div>
      </template>

      <div class="px-4 py-3 flex flex-col gap-2">
        <div
          v-if="addingSection"
          class="flex items-center gap-2 px-2 py-1 border border-dashed border-gray-300 rounded-lg mt-2"
        >
          <input
            class="flex-1 min-w-0 text-sm font-medium text-gray-900 bg-transparent hover:bg-gray-50 focus:bg-gray-50 outline-none rounded-md px-1 py-1.5"
            placeholder="Navn på seksjon"
            v-model="newSectionName"
            :ref="(el) => el && (addSectionNameEl = el)"
            @keydown.enter="confirmAddSection()"
            @keydown.esc="addingSection = false"
          />
          <button
            class="p-1.5 rounded-md text-blue-600 hover:bg-blue-50 flex-shrink-0"
            @click="confirmAddSection()"
          >
            <PlusIcon class="h-4 w-4" />
          </button>
          <div class="w-px self-stretch bg-gray-200 ml-1"></div>
          <button
            class="p-1.5 pl-2.5 rounded-md border-0 shadow-none bg-transparent text-gray-400 hover:bg-gray-100 hover:text-gray-700 focus:outline-none flex-shrink-0"
            @click="addingSection = false"
          >
            <CloseIcon class="h-4 w-4" />
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
import PlusIcon from '@/components/icons/PlusIcon.vue'
import DotsVerticalIcon from '@/components/icons/DotsVerticalIcon.vue'
import HamburgerMenuIcon from '@/components/icons/HamburgerMenuIcon.vue'
import CheckIcon from '@/components/icons/CheckIcon.vue'
import CloseIcon from '@/components/icons/CloseIcon.vue'
import { nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import SecondaryButton from './ui/SecondaryButton.vue'
import CheckBox from './ui/CheckBox.vue'
import EditIcon from './icons/EditIcon.vue'
import CounterInput from './ui/CounterInput.vue'
import CompactProgressBar from '@/components/ui/CompactProgressBar.vue'
import SectionBox from '@/components/SectionBox.vue'
import ActionStrip from '@/components/ActionStrip.vue'
import { useListSession } from '@/composables/useListSession.js'

const items = ref(null)
const supplyTargets = ref(null)
const newItemName = ref('')
const newSectionName = ref('')
const errorMsg = ref(null)
const rootEl = ref(null)

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
    requestAnimationFrame(() => el && el.focus())
  })
}

// These template refs are re-assigned by Vue on every re-render of the row (e.g. when
// quantity changes while editing), but we only want to steal focus once, when the mode
// is *entered* — otherwise every unrelated update (like tapping the quantity stepper)
// yanks focus back to the name field and pops the mobile keyboard back up.
const editItemNameEl = ref(null)
const editSectionNameEl = ref(null)
const addItemNameEl = ref(null)
const addSectionNameEl = ref(null)

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

function toggleTargetPicker(id) {
  targetPickerItemId.value = targetPickerItemId.value === id ? null : id
}

function setSupplyTarget(item, targetId) {
  updateItem(item, 'supply_target_id', targetId)
  targetPickerItemId.value = null
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

const {
  editingItemId,
  editingSectionId,
  movingItemId,
  movingSectionId,
  sectionPickerItemId,
  groupedItems,
  openEdit,
  openEditSection,
  closeEditSection,
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
  renumberAndPersist
} = useListSession({
  list: items,
  rootEl,
  isDesktop,
  persistReorder: (item, newIndex) => updateItem(item, 'index', newIndex),
  onOutsideClick: (target) => {
    if (
      targetPickerItemId.value &&
      !target.closest(`[data-target-picker-owner="${targetPickerItemId.value}"]`)
    ) {
      targetPickerItemId.value = null
      return true
    }
    return false
  }
})

watch(editingItemId, (val) => {
  targetPickerItemId.value = null
  if (val !== null) focusSoon(editItemNameEl.value)
})
watch(editingSectionId, (val) => {
  if (val !== null) focusSoon(editSectionNameEl.value)
})
watch(addingItemSectionId, (val) => {
  if (val !== null) focusSoon(addItemNameEl.value)
})
watch(addingSection, (val) => {
  if (val) focusSoon(addSectionNameEl.value)
})

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

onMounted(async () => {
  desktopMql.addEventListener('change', onMqlChange)

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
})
</script>
