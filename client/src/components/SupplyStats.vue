<template>
  <!-- DESKTOP: vertical panel -->
  <div v-if="realTargets.length" class="hidden md:flex md:flex-col md:gap-3">
    <div class="bg-gray-50 border border-gray-200 rounded-lg p-3">
      <div class="text-[10px] font-bold tracking-wide uppercase text-gray-400">Mål totalt</div>
      <div class="text-lg font-bold tabular-nums text-gray-900">{{ totalCount }}</div>
    </div>

    <div class="bg-gray-50 border border-gray-200 rounded-lg p-3">
      <div class="text-[10px] font-bold tracking-wide uppercase text-gray-400">Fullt dekket</div>
      <div class="text-lg font-bold tabular-nums">
        <span class="text-green-600">{{ coveredCount }}</span>
        <span class="text-gray-400 font-semibold"> / {{ totalCount }}</span>
      </div>
    </div>

    <div v-if="perPerson.length" class="bg-gray-50 border border-gray-200 rounded-lg p-3">
      <div class="text-[10px] font-bold tracking-wide uppercase text-gray-400 mb-2">
        Fordeling per person
      </div>
      <div class="flex flex-col gap-2">
        <div v-for="(p, idx) in perPerson" :key="p.id" class="flex items-center gap-2">
          <AvatarImage :name="p.avatar" :title="p.username" size="5" class="!mx-0 flex-shrink-0" />
          <span class="text-xs text-gray-700 truncate flex-shrink min-w-0 w-14">{{
            p.username
          }}</span>
          <div class="flex-1 h-1.5 rounded-full bg-gray-200 overflow-hidden">
            <div
              class="h-full rounded-full transition-all"
              :style="{ width: (p.total / maxPerson) * 100 + '%', backgroundColor: colorFor(idx) }"
            ></div>
          </div>
          <span class="text-xs font-bold tabular-nums text-gray-900 w-6 text-right">{{
            p.total
          }}</span>
        </div>
      </div>
    </div>
  </div>

  <!-- MOBILE: compact strip -->
  <div v-if="realTargets.length" class="md:hidden flex flex-col gap-2">
    <div class="grid grid-cols-3 gap-2">
      <div class="bg-gray-50 border border-gray-200 rounded-lg p-2 text-center">
        <div class="text-[10px] font-bold tracking-wide uppercase text-gray-400">Mål</div>
        <div class="text-sm font-bold tabular-nums text-gray-900">{{ totalCount }}</div>
      </div>
      <div class="bg-gray-50 border border-gray-200 rounded-lg p-2 text-center">
        <div class="text-[10px] font-bold tracking-wide uppercase text-gray-400">Dekket</div>
        <div class="text-sm font-bold tabular-nums">
          <span class="text-green-600">{{ coveredCount }}</span
          ><span class="text-gray-400">/{{ totalCount }}</span>
        </div>
      </div>
      <div
        v-if="topContributor"
        class="bg-gray-50 border border-gray-200 rounded-lg p-2 text-center"
      >
        <div class="text-[10px] font-bold tracking-wide uppercase text-gray-400">Topp</div>
        <div class="text-sm font-bold truncate text-gray-900">{{ topContributor.username }}</div>
      </div>
    </div>

    <div v-if="perPerson.length" class="flex gap-2 overflow-x-auto">
      <div
        v-for="(p, idx) in perPerson"
        :key="p.id"
        class="flex items-center gap-1.5 bg-gray-50 border border-gray-200 rounded-full px-2 py-1 text-xs whitespace-nowrap flex-shrink-0"
      >
        <AvatarImage :name="p.avatar" :title="p.username" size="4" class="!mx-0" />
        <span class="text-gray-700"
          >{{ p.username }} ·
          <span class="font-bold tabular-nums text-gray-900">{{ p.total }}</span></span
        >
        <span
          class="w-1.5 h-1.5 rounded-full flex-shrink-0"
          :style="{ backgroundColor: colorFor(idx) }"
        ></span>
      </div>
    </div>
  </div>
</template>

<script setup>
import AvatarImage from '@/components/AvatarImage.vue'
import { computed } from 'vue'

const props = defineProps({
  targets: {
    type: Array,
    required: true
  }
})

const PALETTE = ['#3b82f6', '#7c3aed', '#d97706', '#16a34a']

const realTargets = computed(() =>
  (props.targets ?? []).filter((t) => !t.name.startsWith('section:'))
)

const totalCount = computed(() => realTargets.value.length)

const coveredCount = computed(
  () =>
    realTargets.value.filter((t) => {
      if (!(t.target_quantity > 0)) return false
      const sum = t.items.reduce((s, i) => s + i.quantity, 0)
      return sum >= t.target_quantity
    }).length
)

const perPerson = computed(() => {
  const map = new Map()
  for (const t of realTargets.value) {
    for (const item of t.items) {
      const p = item.participant
      if (!p) continue
      const existing = map.get(p.id)
      if (existing) {
        existing.total += item.quantity
      } else {
        map.set(p.id, { id: p.id, username: p.username, avatar: p.avatar, total: item.quantity })
      }
    }
  }
  return [...map.values()].sort((a, b) => b.total - a.total)
})

const maxPerson = computed(() => Math.max(1, ...perPerson.value.map((p) => p.total)))

const topContributor = computed(() => perPerson.value[0] ?? null)

function colorFor(idx) {
  return PALETTE[idx % PALETTE.length]
}
</script>
