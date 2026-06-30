<template>
  <div class="flex flex-col h-screen max-w-md mx-auto border bg-gray-50 shadow-lg rounded-lg overflow-hidden my-4">
    <div class="bg-blue-600 p-4 text-white font-bold flex justify-between items-center">
      <span>Cambodia Tech Shop - ជំនួយការ AI</span>
      <span class="w-3 h-3 bg-green-400 rounded-full animate-pulse"></span>
    </div>

    <div class="flex-1 p-4 overflow-y-auto space-y-3" ref="chatContainer">
      <div 
        v-for="(msg, index) in chatHistory" 
        :key="index" 
        :class="['flex', msg.role === 'user' ? 'justify-end' : 'justify-start']"
      >
        <div 
          :class="[
            'max-w-[75%] rounded-lg p-3 text-sm shadow-sm whitespace-pre-line',
            msg.role === 'user' ? 'bg-blue-500 text-white rounded-br-none' : 'bg-white text-gray-800 border rounded-bl-none'
          ]"
        >
          {{ msg.text }}
        </div>
      </div>

      <div v-if="isLoading" class="flex justify-start">
        <div class="bg-white border rounded-lg p-3 text-sm text-gray-500 italic rounded-bl-none">
          កំពុងវាយអក្សរ...
        </div>
      </div>
    </div>

    <form @submit.prevent="sendMessage" class="p-3 border-t bg-white flex gap-2">
      <input 
        v-model="userInput" 
        type="text" 
        placeholder="សួរអ្វីមួយអំពីហាង..." 
        class="flex-1 border rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-blue-500"
        :disabled="isLoading"
      />
      <button 
        type="submit" 
        class="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-700 transition disabled:opacity-50"
        :disabled="isLoading || !userInput.trim()"
      >
        ផ្ញើ
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'

const userInput = ref('')
const chatHistory = ref([
  { role: 'model', text: 'សួស្តីបាទ! ខ្ញុំជាជំនួយការ AI របស់ហាង Cambodia Tech Shop។ តើខ្ញុំអាចជួយអ្វីលោកអ្នកបានខ្លះបាទ?' }
])
const isLoading = ref(false)
const chatContainer = ref(null)

// មុខងារស្វ័យប្រវត្តរំកិលអេក្រង់ចុះក្រោមពេលមានសារថ្មី
const scrollToBottom = async () => {
  await nextTick()
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  }
}

const sendMessage = async () => {
  if (!userInput.value.trim()) return

  const messageText = userInput.value
  // ១. បន្ថែមសាររបស់អ្នកប្រើប្រាស់ទៅក្នុង UI
  chatHistory.value.push({ role: 'user', text: messageText })
  userInput.value = ''
  isLoading.value = true
  scrollToBottom()

  try {
    // ២. ផ្ញើសំណើទៅកាន់ Flask Backend (Port 5000)
    const response = await fetch('https://chat-bot-shop.onrender.com/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: messageText })
    })

    const data = await response.json()
    
    // ៣. បន្ថែមចម្លើយរបស់ AI ទៅក្នុង UI
    if (data.response) {
      chatHistory.value.push({ role: 'model', text: data.response })
    } else {
      chatHistory.value.push({ role: 'model', text: 'សូមអភ័យទោស មានបញ្ហាបច្ចេកទេសមួយបានកើតឡើង។' })
    }
  } catch (error) {
    console.error('Error:', error)
    chatHistory.value.push({ role: 'model', text: 'មិនអាចភ្ជាប់ទៅកាន់ Server បានទេ។' })
  } finally {
    isLoading.value = false
    scrollToBottom()
  }
}
</script>
