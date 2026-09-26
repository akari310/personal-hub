import { defineConfig } from 'vitepress'

export default defineConfig({
  title: "Personal Hub",
  description: "Startpage & Cheatsheet",
  themeConfig: {
    search: {
      provider: 'local'
    },
    nav: [
      { text: 'Startpage', link: '/' },
      { text: 'Cheatsheet', link: '/notes/' }
    ],
    sidebar: {
      '/notes/': [
        {
          text: 'Cheatsheets',
          items: [
            { text: 'Linux & Servers', link: '/notes/linux' },
            { text: 'Git Commands', link: '/notes/git' },
            { text: 'Docker & Compose', link: '/notes/docker' },
            { text: 'Web Dev Basics', link: '/notes/web-dev' }
          ]
        }
      ]
    },
    socialLinks: [
      { icon: 'github', link: 'https://github.com' }
    ]
  },
  ignoreDeadLinks: true
})
