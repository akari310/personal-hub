import { defineConfig } from 'vitepress'

export default defineConfig({
  router: {
    prefetchLinks: false
  },
  title: "Personal Hub",
  description: "Startpage & Cheatsheet",
  themeConfig: {
    editLink: {
      pattern: 'https://github.com/akari310/personal-hub/edit/main/:path',
      text: 'Sửa trang này trên Github'
    },
    search: {
      provider: 'local'
    },
    nav: [
      { text: 'Bio', link: 'https://akari.nx.kg' },
      { text: 'Hub', link: '/' },
      { text: 'Notes', link: '/notes/' }
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
