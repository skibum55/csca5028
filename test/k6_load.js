import http from 'k6/http'
import { sleep } from 'k6'

export const options = {
  vus: 10,
  duration: '1m',
}

export default function () {
  // Request page containing a form and submit form setting/overriding some fields of the form
  http.get('https://psychic-trout-ppq4r776r5hxg-8000.app.github.dev/')
  http.get('https://psychic-trout-ppq4r776r5hxg-8000.app.github.dev/collect')

  sleep(3)
}