<script>
import { h } from 'vue'
import DraggableItemIcon from '@/components/icons/DraggableItemIcon.vue'
import ArrowUpIcon from '@/components/icons/ArrowUpIcon.vue'
import ArrowDownIcon from '@/components/icons/ArrowDownIcon.vue'
import ArrowRightIcon from '@/components/icons/ArrowRightIcon.vue'
import EditIcon from '@/components/icons/EditIcon.vue'
import TrashIcon from '@/components/icons/TrashIcon.vue'

/* ---------- small local action-menu components (icon + subtle caption, shared style) ---------- */
function menuButtonProps() {
  return {
    isFirst: { type: Boolean, default: false },
    isLast: { type: Boolean, default: false },
    showEdit: { type: Boolean, default: false },
    showMoveTo: { type: Boolean, default: true },
    label: { type: String, default: '' }
  }
}

export default {
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
        [
          h(icon, { class: 'w-5 h-5' }),
          h('span', { class: 'text-[10px] font-semibold text-gray-500' }, label)
        ]
      )
    const children = [btn(DraggableItemIcon, 'Dra', undefined, { grip: true, hideOnMobile: true })]
    children.push(btn(ArrowUpIcon, 'Opp', () => this.$emit('up'), { disabled: this.isFirst }))
    children.push(btn(ArrowDownIcon, 'Ned', () => this.$emit('down'), { disabled: this.isLast }))
    if (this.showMoveTo) {
      children.push(btn(ArrowRightIcon, 'Flytt til', () => this.$emit('move-to-section')))
    }
    if (this.showEdit) {
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
</script>
