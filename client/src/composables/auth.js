import { ref } from 'vue'

const currentUser = ref(null)

export function useAuth() {
  async function logout() {
    const response = await fetch('/api/logout', { method: 'POST' })
    if (!response.ok) return false
    currentUser.value = null
    return true
  }

  async function updateUser() {
    try {
      const response = await fetch('/api/profile')
      if (response.ok) {
        const userData = await response.json()
        currentUser.value = userData
      } else {
        currentUser.value = null
      }
    } catch (error) {
      console.error('Error fetching user data:', error)
      currentUser.value = null
    }
  }

  return { currentUser, logout, updateUser }
}
