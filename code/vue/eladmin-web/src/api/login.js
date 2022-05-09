import request from '@/utils/request'

export function login(username, password, code, uuid) {
  return request({
    url: 'login',
    method: 'post',
    data: {
      username,
      password,
      code,
      uuid
    }
  })
}

export function getInfo() {
  return request({
    url: 'info',
    method: 'get'
  })
}

export function getCodeImg() {
  return request({
    url: 'code',
    method: 'get'
  })
}

export function logout() {
  return request({
    url: 'logout',
    method: 'delete'
  })
}
