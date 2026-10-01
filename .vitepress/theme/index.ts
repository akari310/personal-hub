import DefaultTheme from 'vitepress/theme'
import './style.css'
import Startpage from './components/Startpage.vue'
import SearchBar from './components/SearchBar.vue'
import Layout from './Layout.vue'

export default {
  ...DefaultTheme,
  Layout,
  enhanceApp({ app }) {
    app.component('Startpage', Startpage)
    app.component('SearchBar', SearchBar)
  }
}
