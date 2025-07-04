<template>
  <div class="relative overflow-x-auto">
    <SecondaryButton @click="editMode = !editMode" class="m-2">
      {{ editMode ? 'Lagre' : 'Rediger' }}
    </SecondaryButton>

    <p v-if="!items">
      <ListSkeleton />
    </p>

    <table v-else class="table-fixed text-left text-gray-500 rounded-md">
      <thead
        v-if="!items[0]?.name.startsWith('section:')"
        class="text-xs uppercase text-gray-700 bg-gray-50"
      >
        <tr>
          <th v-if="editMode"></th>
          <th class="px-2 py-2 w-full">Produkt</th>
          <th class="px-1 md:px-6 py-2 max-md:hidden">Forsyningsmål</th>
          <th class="px-1 md:px-6 py-2 whitespace-nowrap">Antall</th>
          <th v-if="!editMode" class="px-1 md:px-6 py-2 whitespace-nowrap">Pakket</th>
          <th v-if="editMode">Slett</th>
        </tr>
      </thead>
      <TransitionGroup name="checklist" tag="tbody">
        <tr v-if="items.length === 0">
          <td colspan="5" class="text-left w-full px-5 py-2">
            <p class="text-md">
              Du har ingenting i pakkelisten din enda! Vil du kopiere listen din fra sist?
            </p>

            <SecondaryButton @click="copyItemsFromOtherTrip()" class="me-2 mt-2"
              >📋 kopier fra sist</SecondaryButton
            >
          </td>
        </tr>

        <template v-for="(item, pos) in items" :key="item.id">
          <tr
            v-if="item.name.startsWith('section:')"
            :class="{
              'border-b-4 border-b-gray-600': dragHoverPosition === pos && dragStartPosition < pos,
              'border-t-4 border-t-gray-600': dragHoverPosition === pos && dragStartPosition > pos,
              'border-b border-b-gray-300': dragHoverPosition !== pos
            }"
            @dragstart="(e) => dragstart_handler(e, pos)"
            @drop="(e) => dropHandler(e, pos)"
            @dragenter.prevent="dragHoverPosition = pos"
            @dragover.prevent
          >
            <td v-if="editMode" draggable="true" class="cursor-pointer pr-0 pt-8 pb-2">
              <DraggableItemIcon />
            </td>
            <td class="px-2 pt-8 pb-2 text-gray-900 font-bold text-xl" :colspan="editMode ? 3 : 4">
              <input
                class="w-full py-0 md:py-1 rounded-sm outline-none"
                :class="{
                  'bg-transparent hover:bg-white cursor-pointer': !item._status?.editing,
                  'bg-gray-50 outline-1 outline-gray-400': item._status?.editing
                }"
                :value="item.name.replace('section:', '')"
                @click="item._status.editing = true"
                @focus="item._status.editing = true"
                @keydown.enter="(event) => editItemName(item, `section:${event.target.value}`)"
                @blur="(event) => editItemName(item, `section:${event.target.value}`)"
              />
            </td>
            <td v-if="editMode" class="px-1 md:px-6 pt-8 pb-2 whitespace-nowrap text-right">
              <button @click="removeItem(item)" class="hover:underline hover:cursor-pointer">
                <CloseIcon class="bg-red w-4 h-4"></CloseIcon>
              </button>
            </td>
          </tr>
          <tr
            v-if="item.name.startsWith('section:')"
            class="w-full text-xs uppercase text-gray-700 bg-gray-50"
          >
            <th v-if="editMode"></th>
            <th class="px-2 py-2 w-full">Produkt</th>
            <th class="px-1 md:px-6 py-2 max-md:hidden">Forsyningsmål</th>
            <th class="px-1 md:px-6 py-2 whitespace-nowrap">Antall</th>
            <th v-if="!editMode" class="px-1 md:px-6 py-2 whitespace-nowrap">Pakket</th>
            <th v-if="editMode">Slett</th>
          </tr>
          <tr
            v-else
            class="checklist-item"
            :class="{
              'border-b-4 border-b-gray-600': dragHoverPosition === pos && dragStartPosition < pos,
              'border-t-4 border-t-gray-600': dragHoverPosition === pos && dragStartPosition > pos,
              'border-b border-b-gray-300': dragHoverPosition !== pos
            }"
            @dragstart="(e) => dragstart_handler(e, pos)"
            @drop="(e) => dropHandler(e, pos)"
            @dragenter.prevent="dragHoverPosition = pos"
            @dragover.prevent
          >
            <td v-if="editMode" draggable="true" class="cursor-pointer pr-0">
              <DraggableItemIcon />
            </td>
            <td class="w-full px-2 py-2 text-gray-900">
              <div>
                <input
                  class="w-full py-0 md:py-1 rounded-sm outline-none"
                  :class="{
                    'bg-transparent hover:bg-white cursor-pointer': !item._status?.editing,
                    'bg-gray-50 outline-1 outline-gray-400': item._status?.editing
                  }"
                  :value="item.name"
                  @click="item._status.editing = true"
                  @focus="item._status.editing = true"
                  @keydown.enter="(event) => editItemName(item, event.target.value)"
                  @blur="(event) => editItemName(item, event.target.value)"
                />
              </div>

              <div class="md:hidden">
                <div class="px-0 py-0 pb-1" v-if="item.supply_target && !editMode">
                  <label class="text-xs"
                    ><span class="md:hidden">Forsyningsmål: </span
                    >{{ item.supply_target?.name }}</label
                  >
                </div>
                <div class="px-0 py-0" v-if="editMode">
                  <select
                    class="text-xs text-blue-600 py-1.5 border-0 appearance-none focus:outline-none focus:ring-0 focus:border-1 focus:border-gray-200"
                    :value="item.supply_target_id"
                    @input="(event) => updateItem(item, 'supply_target_id', event.target.value)"
                  >
                    <option value="" selected>---</option>
                    <option
                      v-for="supplyTarget in supplyTargets"
                      :key="supplyTarget.id"
                      :value="supplyTarget.id"
                      @input="editItemSupplyTarget(item, supplyTarget.id)"
                    >
                      {{ supplyTarget.name }}
                    </option>
                  </select>
                </div>
              </div>
            </td>
            <td class="max-md:hidden px-0 md:px-6 py-2 whitespace-nowrap">
              <div class="px-0 py-0" v-if="item.supply_target && !editMode">
                <label class="text-sm"
                  ><span class="md:hidden">Forsyningsmål:</span
                  >{{ item.supply_target?.name }}</label
                >
              </div>
              <div class="px-0 py-0" v-if="editMode">
                <select
                  class="text-sm text-gray-500 bg-transparent border-0 appearance-none focus:outline-none focus:ring-0 focus:border-gray-200"
                  :value="item.supply_target_id"
                  @input="(event) => updateItem(item, 'supply_target_id', event.target.value)"
                >
                  <option value="" selected>---</option>
                  <option
                    v-for="supplyTarget in supplyTargets"
                    :key="supplyTarget.id"
                    :value="supplyTarget.id"
                    @input="editItemSupplyTarget(item, supplyTarget.id)"
                  >
                    {{ supplyTarget.name }}
                  </option>
                </select>
              </div>
            </td>
            <td class="px-1 md:px-6 py-2 whitespace-nowrap">
              <CounterInput
                :value="item.quantity"
                @update:value="($event) => updateItem(item, 'quantity', $event)"
                :editable="editMode"
              />
            </td>
            <td v-if="!editMode" class="px-1 md:px-6 py-2 whitespace-nowrap">
              <CheckBox
                v-model="item.packed"
                @input="updateItem(item, 'packed', !item.packed)"
              ></CheckBox>
            </td>
            <td v-if="editMode" class="px-1 md:px-6 py-2 whitespace-nowrap text-right">
              <button
                @click="removeItem(item)"
                class="transition-colors hover:text-red-400 hover:cursor-pointer"
              >
                <CloseIcon class="bg-red w-4 h-4"></CloseIcon>
              </button>
            </td>
          </tr>
        </template>
      </TransitionGroup>
    </table>

    <div class="w-full px-6 py-4 font-semibold" ref="addNewRef">
      <div class="relative">
        <TextInput
          class="!p-4 mb-3"
          placeholder="Legg til ny"
          v-model="newItemName"
          :error="errorMsg"
          @keydown.enter="addItem(newItemName)"
          @keydown.esc="errorMsg = null"
        />
        <PrimaryButton
          @click="addItem(newItemName)"
          class="absolute end-2.5 top-2.5 !rounded-full !p-2"
        >
          <PlusIcon class="h-4 w-4" />
        </PrimaryButton>
      </div>
      <SecondaryButton @click="suggestItemName()">✨ Hva med... ✨</SecondaryButton>
    </div>
  </div>
</template>

<script setup>
import ListSkeleton from '@/components/ListSkeleton.vue'
import DraggableItemIcon from '@/components/icons/DraggableItemIcon.vue'
import PlusIcon from '@/components/icons/PlusIcon.vue'
import { scrollIntoView } from '@/components/utils'
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import PrimaryButton from '@/components/ui/PrimaryButton.vue'
import SecondaryButton from './ui/SecondaryButton.vue'
import CheckBox from './ui/CheckBox.vue'
import TextInput from './ui/TextInput.vue'
import CloseIcon from './icons/CloseIcon.vue'
import CounterInput from './ui/CounterInput.vue'

const items = ref(null)
const supplyTargets = ref(null)
const newItemName = ref('')
const addNewRef = ref(null)
const errorMsg = ref(null)
const dragHoverPosition = ref(null)
const dragStartPosition = ref(null)
const remainingSuggestions = ref(null)

const editMode = ref(false)

const params = useRoute().params

const suggestItemName = () => {
  newItemName.value = remainingSuggestions.value.pop() ?? '...godt humør?'
}

Array.prototype.move = function (from, to) {
  this.splice(to, 0, this.splice(from, 1)[0])
  return this
}

function dragstart_handler(event, startPos) {
  dragStartPosition.value = startPos
  event.dataTransfer.setData('startPos', startPos)
  const parentRow = event.target.parentElement
  event.dataTransfer.setDragImage(parentRow, parentRow.width, parentRow.height)
}

function dropHandler(event, dropPos) {
  event.preventDefault()
  items.value.move(event.dataTransfer.getData('startPos'), dropPos)
  dragHoverPosition.value = null

  const prev = items.value[dropPos - 1]?.index || 0
  const next = items.value[dropPos + 1]?.index || 1_000_000_000

  const newIndex = Math.floor((prev + next) / 2)

  updateItem(items.value[dropPos], 'index', newIndex)
}

async function removeItem(item) {
  const response = await fetch(`/api/participant/${params.listId}/items/${item.id}`, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json'
    }
  })

  if (response.ok) items.value = items.value.filter((i) => i.id != item.id)
}

async function addItem(itemName) {
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

  const itemPosition = (items.value.slice(-1)[0]?.index || 0) + 1_000_000

  errorMsg.value = null
  const response = await fetch(`/api/participant/${params.listId}/items`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ name: itemName, index: itemPosition })
  })
  const item = await response.json()
  item._status = {
    editing: false
  }
  console.log(item)
  items.value.push(item)
  newItemName.value = ''

  scrollIntoView(addNewRef.value, 50)
}

function editItemSupplyTarget(item, supplyTargetId) {
  updateItem(item, 'supply_target_id', supplyTargetId)
}

function editItemName(item, newName) {
  if (item._status?.editing) {
    updateItem(item, 'name', newName)
    item._status.editing = false
  }
}

async function updateItem(item, attr, val) {
  try {
    const response = await fetch(`/api/participant/${params.listId}/items/${item.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
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
    headers: {
      'Content-Type': 'application/json'
    },
    body: {}
  })
  if (response.ok) {
    const itemList = await response.json()
    items.value = itemList
      .map((item) => ({
        ...item,
        _status: {
          editing: false
        }
      }))
      .sort((a, b) => a.index - b.index)
  }
}

onMounted(async () => {
  try {
    const response = await fetch(`/api/trip/${params.tripId}/participant/${params.listId}/items`)
    const itemList = await response.json()
    items.value = itemList
      .map((item) => ({
        ...item,
        _status: {
          editing: false
        }
      }))
      .sort((a, b) => a.index - b.index)
    const supplyResponse = await fetch(`/api/trip/${params.tripId}/supply-targets`)
    supplyTargets.value = await supplyResponse.json()
    const suggestionsResponse = await fetch(`/api/items`)
    const suggestions = await suggestionsResponse.json()
    remainingSuggestions.value = suggestions
  } catch (err) {
    return err
  }
})
</script>

<style scoped>
.checklist-move,
.checklist-enter-active,
.checklist-leave-active,
.checklist-item {
  transition:
    all 0.5s ease,
    background-color 0s,
    border-bottom 0.2s,
    border-top 0.2s;
}

.checklist-enter,
.checklist-leave-to {
  opacity: 0;
  transform: translateX(300px);
}

.checklist-leave-active {
  position: absolute;
}
</style>
