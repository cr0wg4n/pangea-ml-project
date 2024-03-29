const QA_URL = "http://192.168.1.13:8000/model"
// const QA_URL = "http://pangea.brickheads.space:8000/model"

const app = new Vue({
  el: '#app',
  data: () => ({
    debug: false,
    chat: false,
    language: 'es',
    country: 'bo',
    userMessage: '',
    messages: [
      {
        image: '/assets/img/logo.png',
        message: '¿Tienes dudas?, yo te puedo ayudar',
        urls: [],
        stars: 0,
        bot: true,
        answer: false,
        debug: {}
      },
      // {
      //   image: 'https://avatars.dicebear.com/api/croodles-neutral/.svg',
      //   message: '¿Donde puedo comer salteñas en cochabamba?',
      //   urls: [],
      //   stars: 0,
      //   bot: false,
      //   answer: false
      // },
      // {
      //   image: '/assets/img/logo.png',
      //   message: 'Salteñeria los Castores',
      //   urls: [
      //     'https://www.los-castores.com/Cochabamba/',
      //   ],
      //   stars: 2,
      //   bot: true,
      //   answer: true
      // },languageo',
      //   urls: [
      //     'https://www.los-castores.com/Cochabamba/'
      //   ],
      //   stars: 3,
      //   bot: true,
      //   answer: true
      // }
    ]
  }),
  created () {
    this.loadData()
  },
  methods: {
    createAnswers (data) {
      data.forEach(item => {
        this.addBotMessage(item.answer.answer, [item.url], item.answer)
      })
      this.scrollChatToBottom()
    },
    async makeQuestion (question) {
      try {
        const response = await fetch(QA_URL, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            question,
            country: this.country,
            language: this.language
          })
        })
        const data = await response.json()
        this.createAnswers(data)
      } catch (error) {
        console.log(error)
        return null
      }
    },
    addBotMessage (message, urls=[], debug={}) {
      debug.urls = urls
      const botMessage = {
        image: '/assets/img/logo.png',
        message,
        urls,
        stars: 0,
        bot:true,
        answer: true,
        debug
      }
      this.messages.push(botMessage)
    },
    scrollChatToBottom () {
      setTimeout(() => {
        let div = document.getElementById('chat')
        div.scrollTop = div.scrollHeight
      }, 100);
    },
    addMessage () {
      const userMessage = {
        image: 'https://avatars.dicebear.com/api/croodles-neutral/.svg',
        message: this.userMessage,
        urls: [],
        stars: 0,
        bot: false,
        answer: false
      }
      this.messages.push(userMessage)
      this.makeQuestion(this.userMessage)
      this.scrollChatToBottom()
      this.userMessage = ''
    },
    shortUrl (url, n=30){
      return url.substring(0, n) + '...'
    },
    assingStar (messageId, stars=5)
    {
      this.messages[messageId].stars = parseInt(6-stars)
    },
    loadData () {
      const colorScale = d3.scaleSequentialSqrt(d3.interpolateYlOrRd)
      // GDP per capita (avoiding countries with small pop)
      const getVal = feat => feat.properties.GDP_MD_EST / Math.max(1e5, feat.properties.POP_EST)
      // https://s3.us-east-1.amazonaws.com/hdx-production-filestore/resources/3dcacf9a-df39-45e3-86a8-4bcd74477b77/bolivia.geojson
      // https://globe.gl/example/datasets/ne_110m_admin_0_countries.geojson
      fetch('./countries.geojson').then(res => res.json()).then(countries =>
        {
          const maxVal = Math.max(...countries.features.map(getVal))
          colorScale.domain([0, maxVal])
          const baseColor = '#6969dd'
          const clickColor = '#6E9B34'
          const world = Globe()
            (document.getElementById('globeViz'))
            .globeImageUrl('//unpkg.com/three-globe/example/img/earth-blue-marble.jpg')
            .bumpImageUrl('//unpkg.com/three-globe/example/img/earth-topology.png')
            .backgroundImageUrl('//unpkg.com/three-globe/example/img/night-sky.png')
            .lineHoverPrecision(0)
            // .polygonsData(countries.features.filter(d => d.properties.ISO_A2 !== 'AQ'))
            .polygonsData(countries.features.filter(d =>  d.properties.ABBREV == 'Bolivia'))
            .polygonAltitude(0.24)
            .polygonCapColor(feat => colorScale(getVal(feat)))
            .polygonSideColor(() => 'rgba(255, 255, 255, 0.15)')
            .polygonCapColor(() => baseColor)
            .polygonStrokeColor(() => '#111')
            .polygonLabel(({ properties: d }) => `
              <b>${d.ADMIN} (${d.ISO_A2})</b> <br />
            `)
            // .polygonLabel(({ properties: d }) => `
            //   <b>${d.ADMIN} (${d.ISO_A2}):</b> <br />
            //   GDP: <i>${d.GDP_MD_EST}</i> M$<br/>
            //   Population: <i>${d.POP_EST}</i>
            // `)
            .onPolygonHover(hoverD => world
              .polygonAltitude(d => d === hoverD ? 0.9 : 0.24)
              .polygonCapColor(d => d === hoverD ? 'steelblue' : baseColor)
              // .polygonCapColor(d => d === hoverD ? 'steelblue' : colorScale(getVal(d)))
            )
            .onPolygonClick(click => {
              world.polygonCapColor(d => d == click ? clickColor : 'white')
              this.chat = true
            }
            )
            .polygonsTransitionDuration(300)
      
          world.pointOfView({
            lat: -18.995060,
            lng: -75.764779, 
            altitude: 3})
      })
    }
  }
})
