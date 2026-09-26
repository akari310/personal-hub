import DefaultTheme from 'vitepress/theme'
import './style.css'
import Startpage from './components/Startpage.vue'
import SearchBar from './components/SearchBar.vue'
import GoLinks from './components/GoLinks.vue'

export default {
  ...DefaultTheme,
  enhanceApp({ app }) {
    app.component('Startpage', Startpage)
    app.component('SearchBar', SearchBar)
    app.component('GoLinks', GoLinks)
  }
}
