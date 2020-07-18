import axois from 'axios'

const config = {
  baseURL: '/api',
  timeout: 100000
}

const client = axois.create(config)

export default {
  getHw: (time) =>
    client.get(`?now=${time}`),
  getTags: () =>
    client.get('tags/'),
  getSubjects: () =>
    client.get('subjects/'),
  putHw: (text, tag, subject, time, user, pass) =>
    client.put('/', {
      text: text,
      tag: tag,
      subject: subject,
      time: time,
      username: user,
      password: pass
    }),
  delHw: (id, user, pass) =>
    client.delete('/', {
      data: {
        id: id,
        username: user,
        password: pass
      }
    }),
  postHw: (id, text, tag, subject, time, user, pass) =>
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
