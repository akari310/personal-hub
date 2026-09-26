import { ref, watch } from 'vue'

export const showWeather = ref(typeof localStorage !== 'undefined' ? localStorage.getItem('showWeather') !== 'false' : true)
export const showLinks = ref(typeof localStorage !== 'undefined' ? localStorage.getItem('showLinks') !== 'false' : true)
export const githubToken = ref(typeof localStorage !== 'undefined' ? localStorage.getItem('gh_admin_token') || '' : '')
export const isAdmin = ref(!!githubToken.value)
export const showSettingsPanel = ref(false)

if (typeof window !== 'undefined') {
  watch(showWeather, (val) => localStorage.setItem('showWeather', val.toString()))
  watch(showLinks, (val) => localStorage.setItem('showLinks', val.toString()))
}
