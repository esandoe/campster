<template>
  <div class="flex flex-col md:flex-row md:items-start md:gap-5">
    <aside class="md:order-2 md:w-64 md:flex-shrink-0 md:sticky md:top-4">
      <SupplyStats :targets="targets" />
    </aside>

    <div class="md:order-1 md:flex-1 min-w-0">
      <div
        ref="rootEl"
        class="relative"
        :class="{ 'pb-16': editingItemId || editingSectionId || movingItemId || movingSectionId }"
      >
        <ListSkeleton v-if="targets === null" />

        <template v-else>
          <p
            v-if="!editingItemId && !editingSectionId && !movingItemId && !movingSectionId"
            class="text-center text-xs text-gray-400 px-6 py-2 md:hidden"
          >
            Trykk og hold en rad eller gruppe for å åpne menyen
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
                  ? 'Du redigerer — trykk en annen rad for å fortsette der, eller avslutt når du er ferdig.'
                  : 'Du sorterer — trykk en annen rad eller gruppe for å flytte den i stedet, eller dra i ⠿.'
              }}
            </p>
            <div class="flex items-center justify-center gap-3">
              <div
                class="flex items-center bg-white border border-blue-200 rounded-full p-0.5 gap-0.5"
              >
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

          <template v-for="group in orderedGroups" :key="group.marker?.id ?? 'ungrouped'">
            <!-- grouped sections render inside a box -->
            <SectionBox
              v-if="group.marker"
              :pinned="group.pinned"
              class="relative mb-3"
              :data-section-wrap="group.pinned ? undefined : group.marker.id"
            >
              <template #header>
                <div class="flex items-center justify-between gap-3 section-header">
                  <div class="flex items-center gap-1.5 min-w-0 flex-1">
                    <template v-if="group.pinned">
                      <span class="flex-shrink-0">📌</span>
                      <span class="font-bold text-gray-900 truncate">Soveplasser</span>
                    </template>
                    <template v-else>
                      <input
                        v-if="editingSectionId === group.marker.id"
                        class="flex-1 min-w-0 font-bold text-gray-900 bg-transparent hover:bg-white focus:bg-white outline-none rounded-md px-1 py-0.5 border border-gray-200 truncate"
                        :value="markerLabel(group.marker)"
                        :ref="(el) => el && editingSectionId === group.marker.id && focusSoon(el)"
                        @keydown.enter="(e) => e.target.blur()"
                        @blur="(e) => renameSection(group.marker, e.target.value)"
                      />
                      <div
                        v-else
                        class="flex-1 min-w-0 font-bold text-gray-900 truncate rounded-md px-1 py-0.5"
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
                        {{ markerLabel(group.marker) }}
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
                    </template>
                  </div>
                  <div v-if="group.items.length" class="flex items-center gap-2 flex-shrink-0">
                    <span class="text-xs text-gray-500 whitespace-nowrap">
                      {{ groupSum(group) }}/{{ groupTargetSum(group) }}
                    </span>
                    <div class="w-16">
                      <CompactProgressBar
                        :percent="groupPercent(group)"
                        :variant="groupPercent(group) >= 100 ? 'green' : 'blue'"
                      />
                    </div>
                    <span class="text-xs font-semibold text-gray-500 w-8 text-right"
                      >{{ Math.round(groupPercent(group)) }}%</span
                    >
                  </div>
                </div>
              </template>

              <div
                :data-items-list="group.marker.id"
                :class="{ 'opacity-30': !group.pinned && movingSectionId === group.marker.id }"
              >
                <div
                  v-for="(t, idx) in group.items"
                  :key="t.id"
                  class="relative"
                  :class="{ 'border-b border-gray-100': idx < group.items.length - 1 }"
                  :data-wrap="t.id"
                >
                  <div
                    v-if="editingItemId === t.id"
                    class="flex items-center gap-2 px-1 py-2 bg-gray-50"
                  >
                    <input
                      class="flex-1 min-w-0 text-sm font-medium text-gray-900 bg-transparent hover:bg-white focus:bg-white outline-none rounded-md px-1 py-0.5"
                      :value="t.name"
                      :ref="(el) => el && editingItemId === t.id && focusSoon(el)"
                      @keydown.enter="(e) => e.target.blur()"
                      @blur="(e) => editTargetName(t, e.target.value)"
                    />
                    <CounterInput
                      :value="t.target_quantity"
                      :editable="true"
                      @update:value="(v) => updateTarget(t, 'target_quantity', v)"
                    />
                    <select
                      class="text-sm text-gray-700 bg-transparent border border-gray-200 rounded-md px-1.5 py-1 outline-none focus:border-blue-400"
                      :value="t.unit || ''"
                      @change="(e) => updateTarget(t, 'unit', e.target.value || null)"
                    >
                      <option value="">—</option>
                      <option value="stk">stk</option>
                      <option value="kg">kg</option>
                      <option value="g">g</option>
                      <option value="l">l</option>
                      <option value="dl">dl</option>
                      <option value="m">m</option>
                      <option value="par">par</option>
                      <option value="pk">pk</option>
                      <option value="boks">boks</option>
                      <option value="pose">pose</option>
                    </select>
                    <button
                      class="p-1.5 rounded-md text-gray-400 hover:bg-gray-100 hover:text-gray-700 flex-shrink-0"
                      @click="closeEdit()"
                    >
                      <CheckIcon class="h-4 w-4" />
                    </button>
                  </div>

                  <div
                    v-else
                    class="flex items-center gap-3 px-1 py-2"
                    :class="[
                      { 'opacity-35': movingItemId === t.id },
                      editingItemId !== null || movingItemId !== null
                        ? 'cursor-pointer hover:bg-gray-50'
                        : ''
                    ]"
                    @click="onRowClick(t)"
                  >
                    <SupplyRing :percent="percentOf(t)" />
                    <div class="flex-1 min-w-0">
                      <div class="font-semibold text-sm text-gray-900 truncate">{{ t.name }}</div>
                      <div class="text-xs text-gray-500 truncate">
                        <template v-if="contributorsOf(t).length">
                          <span class="inline-flex items-center -space-x-1 align-middle mr-1">
                            <AvatarImage
                              v-for="entry in contributorsOf(t)"
                              :key="entry.id"
                              :name="entry.participant.avatar"
                              :title="entry.participant.username"
                              size="4"
                            />
                          </span>
                          {{
                            contributorsOf(t)
                              .map((entry) => entry.participant.username)
                              .join(', ')
                          }}
                        </template>
                        <template v-else>—</template>
                      </div>
                    </div>
                    <div class="flex items-center gap-1.5 flex-shrink-0" @click.stop>
                      <div class="text-sm tabular-nums whitespace-nowrap text-right">
                        <span class="font-bold text-gray-900">{{ sumOf(t) }}</span>
                        <span class="text-gray-500"> / {{ t.target_quantity }}</span>
                        <span v-if="t.unit" class="text-gray-400">&nbsp;{{ t.unit }}</span>
                      </div>
                      <button
                        v-if="isDesktop && (editingItemId || editingSectionId)"
                        class="p-1.5 rounded-md text-gray-400 hover:bg-gray-100 hover:text-gray-700 flex-shrink-0"
                        @click.stop="openEdit(t.id)"
                      >
                        <EditIcon />
                      </button>
                      <button
                        v-else-if="isDesktop"
                        class="p-1.5 rounded-md text-gray-400 hover:bg-gray-100 hover:text-gray-700 flex-shrink-0"
                        @click.stop="toggleItemOverlay(t.id)"
                      >
                        <DotsVerticalIcon />
                      </button>
                    </div>
                  </div>

                  <div
                    v-if="movingItemId === t.id"
                    class="move-overlay absolute inset-0 flex items-center justify-center bg-gray-900/45 rounded-md z-50"
                    :data-move-overlay="'item:' + t.id"
                    @click.self="closeItemOverlay()"
                  >
                    <div
                      v-if="sectionPickerItemId === t.id"
                      class="bg-white border-2 border-gray-300 rounded-2xl shadow-2xl p-2 min-w-[200px] max-w-[260px]"
                    >
                      <div class="px-2 pt-1 pb-1 text-xs font-semibold text-gray-500">
                        Flytt til gruppe
                      </div>
                      <button
                        v-for="g in otherSections(t)"
                        :key="g.marker.id"
                        class="flex items-center px-2.5 py-2 rounded-md hover:bg-gray-100 w-full text-left text-sm text-gray-900"
                        @click="moveItemToSection(t, g.marker)"
                      >
                        {{ markerLabel(g.marker) }}
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
                      :is-first="group.items[0]?.id === t.id"
                      :is-last="group.items[group.items.length - 1]?.id === t.id"
                      :show-edit="true"
                      :label="t.name"
                      @up="moveItem(group, t, -1)"
                      @down="moveItem(group, t, 1)"
                      @edit="openEdit(t.id)"
                      @delete="removeTarget(t)"
                      @move-to-section="sectionPickerItemId = t.id"
                    />
                  </div>
                </div>
              </div>

              <div class="px-1 pb-1">
                <div
                  v-if="addingTargetGroupKey === groupKey(group)"
                  class="flex items-center gap-2 px-2 py-1.5 border-t border-dashed border-gray-200 mt-1"
                >
                  <input
                    class="flex-1 min-w-0 text-sm font-medium text-gray-900 bg-transparent hover:bg-gray-50 focus:bg-gray-50 outline-none rounded-md px-1 py-1"
                    placeholder="Navn på mål"
                    v-model="newTargetName"
                    :ref="(el) => el && addingTargetGroupKey === groupKey(group) && focusSoon(el)"
                    @keydown.enter="confirmAddTargetToGroup(group)"
                    @keydown.esc="cancelAddTarget()"
                  />
                  <input
                    type="number"
                    min="0"
                    class="w-16 text-sm text-gray-900 bg-transparent hover:bg-gray-50 focus:bg-gray-50 outline-none rounded-md px-1 py-1 border border-gray-200"
                    placeholder="Mål"
                    v-model="newTargetQty"
                    @keydown.enter="confirmAddTargetToGroup(group)"
                    @keydown.esc="cancelAddTarget()"
                  />
                  <button
                    class="p-1.5 rounded-md text-gray-400 hover:bg-gray-100 hover:text-gray-700 flex-shrink-0"
                    @click="confirmAddTargetToGroup(group)"
                  >
                    <PlusIcon class="h-4 w-4" />
                  </button>
                </div>
                <button
                  v-else
                  class="w-full text-left px-2 py-1.5 text-sm font-semibold text-gray-500 hover:bg-gray-50 hover:text-blue-600 border-t border-dashed border-gray-200 mt-1"
                  @click="startAddTargetToGroup(group)"
                >
                  + Legg til mål
                </button>
              </div>

              <template #overlay>
                <div
                  v-if="!group.pinned && movingSectionId === group.marker.id"
                  class="move-overlay absolute inset-0 flex items-center justify-center bg-gray-900/45 rounded-md z-50"
                  :data-move-overlay="'section:' + group.marker.id"
                  @click.self="movingSectionId = null"
                >
                  <ActionStrip
                    :is-first="isFirstSection(group.marker)"
                    :is-last="isLastSection(group.marker)"
                    :show-edit="true"
                    :show-move-to="false"
                    :label="markerLabel(group.marker)"
                    @up="moveSection(group.marker, -1)"
                    @down="moveSection(group.marker, 1)"
                    @edit="openEditSection(group.marker.id)"
                    @delete="deleteSection(group.marker)"
                  />
                </div>
              </template>
            </SectionBox>

            <!-- ungrouped targets render bare (no box) -->
            <div v-else class="relative mb-3">
              <div :data-items-list="'none'">
                <div
                  v-for="(t, idx) in group.items"
                  :key="t.id"
                  class="relative"
                  :class="{ 'border-b border-gray-100': idx < group.items.length - 1 }"
                  :data-wrap="t.id"
                >
                  <div
                    v-if="editingItemId === t.id"
                    class="flex items-center gap-2 px-1 py-2 bg-gray-50"
                  >
                    <input
                      class="flex-1 min-w-0 text-sm font-medium text-gray-900 bg-transparent hover:bg-white focus:bg-white outline-none rounded-md px-1 py-0.5"
                      :value="t.name"
                      :ref="(el) => el && editingItemId === t.id && focusSoon(el)"
                      @keydown.enter="(e) => e.target.blur()"
                      @blur="(e) => editTargetName(t, e.target.value)"
                    />
                    <CounterInput
                      :value="t.target_quantity"
                      :editable="true"
                      @update:value="(v) => updateTarget(t, 'target_quantity', v)"
                    />
                    <select
                      class="text-sm text-gray-700 bg-transparent border border-gray-200 rounded-md px-1.5 py-1 outline-none focus:border-blue-400"
                      :value="t.unit || ''"
                      @change="(e) => updateTarget(t, 'unit', e.target.value || null)"
                    >
                      <option value="">—</option>
                      <option value="stk">stk</option>
                      <option value="kg">kg</option>
                      <option value="g">g</option>
                      <option value="l">l</option>
                      <option value="dl">dl</option>
                      <option value="m">m</option>
                      <option value="par">par</option>
                      <option value="pk">pk</option>
                      <option value="boks">boks</option>
                      <option value="pose">pose</option>
                    </select>
                    <button
                      class="p-1.5 rounded-md text-gray-400 hover:bg-gray-100 hover:text-gray-700 flex-shrink-0"
                      @click="closeEdit()"
                    >
                      <CheckIcon class="h-4 w-4" />
                    </button>
                  </div>

                  <div
                    v-else
                    class="flex items-center gap-3 px-1 py-2"
                    :class="[
                      { 'opacity-35': movingItemId === t.id },
                      editingItemId !== null || movingItemId !== null
                        ? 'cursor-pointer hover:bg-gray-50'
                        : ''
                    ]"
                    @click="onRowClick(t)"
                  >
                    <SupplyRing :percent="percentOf(t)" />
                    <div class="flex-1 min-w-0">
                      <div class="font-semibold text-sm text-gray-900 truncate">{{ t.name }}</div>
                      <div class="text-xs text-gray-500 truncate">
                        <template v-if="contributorsOf(t).length">
                          <span class="inline-flex items-center -space-x-1 align-middle mr-1">
                            <AvatarImage
                              v-for="entry in contributorsOf(t)"
                              :key="entry.id"
                              :name="entry.participant.avatar"
                              :title="entry.participant.username"
                              size="4"
                            />
                          </span>
                          {{
                            contributorsOf(t)
                              .map((entry) => entry.participant.username)
                              .join(', ')
                          }}
                        </template>
                        <template v-else>—</template>
                      </div>
                    </div>
                    <div class="flex items-center gap-1.5 flex-shrink-0" @click.stop>
                      <div class="text-sm tabular-nums whitespace-nowrap text-right">
                        <span class="font-bold text-gray-900">{{ sumOf(t) }}</span>
                        <span class="text-gray-500"> / {{ t.target_quantity }}</span>
                        <span v-if="t.unit" class="text-gray-400">&nbsp;{{ t.unit }}</span>
                      </div>
                      <button
                        v-if="isDesktop && (editingItemId || editingSectionId)"
                        class="p-1.5 rounded-md text-gray-400 hover:bg-gray-100 hover:text-gray-700 flex-shrink-0"
                        @click.stop="openEdit(t.id)"
                      >
                        <EditIcon />
                      </button>
                      <button
                        v-else-if="isDesktop"
                        class="p-1.5 rounded-md text-gray-400 hover:bg-gray-100 hover:text-gray-700 flex-shrink-0"
                        @click.stop="toggleItemOverlay(t.id)"
                      >
                        <DotsVerticalIcon />
                      </button>
                    </div>
                  </div>

                  <div
                    v-if="movingItemId === t.id"
                    class="move-overlay absolute inset-0 flex items-center justify-center bg-gray-900/45 rounded-md z-50"
                    :data-move-overlay="'item:' + t.id"
                    @click.self="closeItemOverlay()"
                  >
                    <div
                      v-if="sectionPickerItemId === t.id"
                      class="bg-white border-2 border-gray-300 rounded-2xl shadow-2xl p-2 min-w-[200px] max-w-[260px]"
                    >
                      <div class="px-2 pt-1 pb-1 text-xs font-semibold text-gray-500">
                        Flytt til gruppe
                      </div>
                      <button
                        v-for="g in otherSections(t)"
                        :key="g.marker.id"
                        class="flex items-center px-2.5 py-2 rounded-md hover:bg-gray-100 w-full text-left text-sm text-gray-900"
                        @click="moveItemToSection(t, g.marker)"
                      >
                        {{ markerLabel(g.marker) }}
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
                      :is-first="group.items[0]?.id === t.id"
                      :is-last="group.items[group.items.length - 1]?.id === t.id"
                      :show-edit="true"
                      :label="t.name"
                      @up="moveItem(group, t, -1)"
                      @down="moveItem(group, t, 1)"
                      @edit="openEdit(t.id)"
                      @delete="removeTarget(t)"
                      @move-to-section="sectionPickerItemId = t.id"
                    />
                  </div>
                </div>
              </div>
            </div>
          </template>

          <div class="flex flex-col gap-2 mt-2">
            <div
              v-if="addingBottomTarget"
              class="flex items-center gap-2 px-2 py-1.5 border border-dashed border-gray-300 rounded-lg"
            >
              <input
                class="flex-1 min-w-0 text-sm font-medium text-gray-900 bg-transparent hover:bg-gray-50 focus:bg-gray-50 outline-none rounded-md px-1 py-1"
                placeholder="Navn på mål"
                v-model="newBottomTargetName"
                :ref="(el) => el && addingBottomTarget && focusSoon(el)"
                @keydown.enter="confirmAddUngroupedTarget()"
                @keydown.esc="addingBottomTarget = false"
              />
              <input
                type="number"
                min="0"
                class="w-16 text-sm text-gray-900 bg-transparent hover:bg-gray-50 focus:bg-gray-50 outline-none rounded-md px-1 py-1 border border-gray-200"
                placeholder="Mål"
                v-model="newBottomTargetQty"
                @keydown.enter="confirmAddUngroupedTarget()"
                @keydown.esc="addingBottomTarget = false"
              />
              <button
                class="p-1.5 rounded-md text-gray-400 hover:bg-gray-100 hover:text-gray-700 flex-shrink-0"
                @click="confirmAddUngroupedTarget()"
              >
                <PlusIcon class="h-4 w-4" />
              </button>
            </div>
            <button
              v-else
              class="w-full text-left px-4 py-2.5 text-sm font-semibold text-gray-500 hover:bg-gray-50 hover:text-blue-600 border border-dashed border-gray-300 rounded-lg"
              @click="startAddBottomTarget()"
            >
              + Legg til mål
            </button>

            <div
              v-if="addingBottomGroup"
              class="flex items-center gap-2 px-2 py-1.5 border border-dashed border-gray-300 rounded-lg"
            >
              <input
                class="flex-1 min-w-0 text-sm font-medium text-gray-900 bg-transparent hover:bg-gray-50 focus:bg-gray-50 outline-none rounded-md px-1 py-1"
                placeholder="Navn på gruppe"
                v-model="newBottomGroupName"
                :ref="(el) => el && addingBottomGroup && focusSoon(el)"
                @keydown.enter="confirmAddGroup()"
                @keydown.esc="addingBottomGroup = false"
              />
              <button
                class="p-1.5 rounded-md text-gray-400 hover:bg-gray-100 hover:text-gray-700 flex-shrink-0"
                @click="confirmAddGroup()"
              >
                <PlusIcon class="h-4 w-4" />
              </button>
            </div>
            <button
              v-else
              class="w-full text-left px-4 py-2.5 text-sm font-semibold text-gray-500 hover:bg-gray-50 hover:text-blue-600 border border-dashed border-gray-300 rounded-lg"
              @click="startAddBottomGroup()"
            >
              + Ny gruppe
            </button>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import ActionStrip from '@/components/ActionStrip.vue'
import AvatarImage from '@/components/AvatarImage.vue'
import ListSkeleton from '@/components/ListSkeleton.vue'
import SectionBox from '@/components/SectionBox.vue'
import SupplyRing from '@/components/SupplyRing.vue'
import SupplyStats from '@/components/SupplyStats.vue'
import CompactProgressBar from '@/components/ui/CompactProgressBar.vue'
import CounterInput from '@/components/ui/CounterInput.vue'
import CheckIcon from '@/components/icons/CheckIcon.vue'
import DotsVerticalIcon from '@/components/icons/DotsVerticalIcon.vue'
import EditIcon from '@/components/icons/EditIcon.vue'
import HamburgerMenuIcon from '@/components/icons/HamburgerMenuIcon.vue'
import PlusIcon from '@/components/icons/PlusIcon.vue'
import { useListSession } from '@/composables/useListSession.js'
import { computed, nextTick, onBeforeUnmount, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'

const SOVE = 'section:Soveplasser'

const targets = ref(null)
const tripId = useRoute().params.tripId
const rootEl = ref(null)

const addingTargetGroupKey = ref(null)
const newTargetName = ref('')
const newTargetQty = ref('')

const addingBottomTarget = ref(false)
const newBottomTargetName = ref('')
const newBottomTargetQty = ref('')

const addingBottomGroup = ref(false)
const newBottomGroupName = ref('')

const isDesktop = ref(window.matchMedia('(min-width: 768px)').matches)
const desktopMql = window.matchMedia('(min-width: 768px)')
function onMqlChange(e) {
  isDesktop.value = e.matches
}

// Focusing an input right as it's mounted can lose to the browser resetting focus
// to <body> when the element it replaces (e.g. an "add" button) is removed in the
// same patch, so wait for Vue's DOM update to fully settle first.
function focusSoon(el) {
  nextTick(() => {
    requestAnimationFrame(() => el.focus())
  })
}

const markerLabel = (t) => t.name.replace(/^section:/, '')
const sumOf = (t) => t.items.reduce((s, i) => s + i.quantity, 0)
const percentOf = (t) => (t.target_quantity > 0 ? (sumOf(t) / t.target_quantity) * 100 : 0)
const contributorsOf = (t) => {
  const map = new Map()
  for (const item of t.items) {
    const p = item.participant
    if (!p) continue
    const existing = map.get(p.id)
    if (existing) existing.quantity += item.quantity
    else map.set(p.id, { id: p.id, participant: p, quantity: item.quantity })
  }
  return [...map.values()]
}

function sortTargets() {
  targets.value = [...targets.value].sort((a, b) => a.index - b.index)
}

function editTargetName(t, newName) {
  updateTarget(t, 'name', newName)
}
function renameSection(marker, newTitle) {
  updateTarget(marker, 'name', 'section:' + (newTitle.trim() || markerLabel(marker)))
}

async function updateTarget(t, attr, val) {
  // The backend replaces the whole row on every PUT (no partial updates), so the request
  // body is built from the current local target. Apply the change locally *before* awaiting
  // the request, same reasoning as TripChecklist.updateItem.
  t[attr] = val
  try {
    const response = await fetch(`/api/trip/${tripId}/supply-targets/${t.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...t, [attr]: val })
    })
    const saved = await response.json()
    // The PUT response has no `items`, so only scalar fields are synced back here.
    t.name = saved.name
    t.target_quantity = saved.target_quantity
    t.index = saved.index
    if ('unit' in saved) t.unit = saved.unit
  } catch (err) {
    return err
  }
}

async function removeTarget(t) {
  const response = await fetch(`/api/trip/${tripId}/supply-targets/${t.id}`, {
    method: 'DELETE',
    headers: { 'Content-Type': 'application/json' }
  })
  if (response.ok) targets.value = targets.value.filter((x) => x.id !== t.id)
  closeItemOverlay()
}

async function deleteSection(marker) {
  await removeTarget(marker)
  movingSectionId.value = null
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
  list: targets,
  rootEl,
  isDesktop,
  persistReorder: (t, idx) => updateTarget(t, 'index', idx),
  isSectionLocked: (marker) => marker.name === SOVE
})

const orderedGroups = computed(() => {
  const groups = groupedItems.value
  const sove = groups.find((g) => g.marker && g.marker.name === SOVE)
  const ungrouped = groups.find((g) => !g.marker)
  const others = groups.filter((g) => g.marker && g !== sove)
  const out = []
  if (sove) out.push({ ...sove, pinned: true })
  out.push(...others)
  if (ungrouped && ungrouped.items.length) out.push({ ...ungrouped, ungrouped: true })
  return out
})

function groupKey(group) {
  return group.marker?.id ?? 'ungrouped'
}

const groupSum = (g) => g.items.reduce((s, t) => s + sumOf(t), 0)
const groupTargetSum = (g) => g.items.reduce((s, t) => s + t.target_quantity, 0)
const groupPercent = (g) => (groupTargetSum(g) > 0 ? (groupSum(g) / groupTargetSum(g)) * 100 : 0)

const maxIndex = () => (targets.value.length ? Math.max(...targets.value.map((t) => t.index)) : 0)
const minIndex = () => (targets.value.length ? Math.min(...targets.value.map((t) => t.index)) : 0)

async function postSupplyTarget(body) {
  const response = await fetch(`/api/trip/${tripId}/supply-targets`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  })
  const created = await response.json()
  return { ...created, items: created.items ?? [], unit: created.unit ?? null }
}

async function ensureSoveplasser() {
  if (targets.value.some((t) => t.name === SOVE)) return
  const created = await postSupplyTarget({
    name: SOVE,
    target_quantity: 0,
    index: maxIndex() + 1_000_000
  })
  targets.value.push(created)
  sortTargets()
}

async function addGroup(name) {
  const created = await postSupplyTarget({
    name: 'section:' + name.trim(),
    target_quantity: 0,
    index: maxIndex() + 1_000_000
  })
  targets.value.push(created)
  sortTargets()
}

async function addTargetToGroup(group, name, targetQuantity) {
  const lastItem = group.items[group.items.length - 1] ?? group.marker
  const posInFlat = targets.value.indexOf(lastItem)
  const nextT = targets.value[posInFlat + 1]
  const newIndex = nextT
    ? Math.floor((lastItem.index + nextT.index) / 2)
    : lastItem.index + 1_000_000
  const created = await postSupplyTarget({
    name,
    target_quantity: targetQuantity || 0,
    index: newIndex
  })
  targets.value.splice(posInFlat + 1, 0, created)
  sortTargets()
  await renumberAndPersist()
}

async function addUngroupedTarget(name, targetQuantity) {
  const newIndex = targets.value.length ? minIndex() - 1_000 : 1_000_000
  const created = await postSupplyTarget({
    name,
    target_quantity: targetQuantity || 0,
    index: newIndex
  })
  targets.value.push(created)
  sortTargets()
}

function startAddTargetToGroup(group) {
  addingTargetGroupKey.value = groupKey(group)
  newTargetName.value = ''
  newTargetQty.value = ''
}

function cancelAddTarget() {
  addingTargetGroupKey.value = null
}

async function confirmAddTargetToGroup(group) {
  const name = newTargetName.value.trim()
  if (!name) return
  await addTargetToGroup(group, name, Number(newTargetQty.value) || 0)
  addingTargetGroupKey.value = null
}

function startAddBottomTarget() {
  addingBottomTarget.value = true
  newBottomTargetName.value = ''
  newBottomTargetQty.value = ''
}

async function confirmAddUngroupedTarget() {
  const name = newBottomTargetName.value.trim()
  if (!name) return
  await addUngroupedTarget(name, Number(newBottomTargetQty.value) || 0)
  addingBottomTarget.value = false
}

function startAddBottomGroup() {
  addingBottomGroup.value = true
  newBottomGroupName.value = ''
}

async function confirmAddGroup() {
  const name = newBottomGroupName.value.trim()
  if (!name) return
  await addGroup(name)
  addingBottomGroup.value = false
}

onMounted(async () => {
  desktopMql.addEventListener('change', onMqlChange)

  try {
    const response = await fetch(`/api/trip/${tripId}/supply-targets`)
    const list = await response.json()
    targets.value = list.sort((a, b) => a.index - b.index)
    await ensureSoveplasser()
  } catch (err) {
    return err
  }
})

onBeforeUnmount(() => {
  desktopMql.removeEventListener('change', onMqlChange)
})
</script>
