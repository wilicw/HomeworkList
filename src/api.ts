import axois from 'axios'

const config = {
  baseURL: 'http://127.0.0.1:5000/api',
  timeout: 100000
}

const client = axois.create(config)

export default {
  getHw: (time: number) =>
    client.get(`?now=${time}`),
  getTags: () =>
    client.get('tags/'),
  getSubjects: () =>
    client.get('subjects/'),
  putHw: (text: string, tag: number, subject: number, time: number, user: string, pass: string) =>
    client.put('/', {
      text: text,
      tag: tag,
      subject: subject,
      time: time,
      username: user,
      password: pass
    }),
  delHw: (id: number, user: string, pass: string) =>
    client.delete('/', {
      data: {
        id: id,
        username: user,
        password: pass
      }
    }),
  postHw: (id: number, text: string, tag: number, subject: number, time: number, user: string, pass: string) =>
    client.post('/', {
      id: id,
      text: text,
      tag: tag,
      subject: subject,
      time: time,
      username: user,
      password: pass
    })
}
