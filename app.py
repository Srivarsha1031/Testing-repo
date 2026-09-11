
// Testing-repo — Sekura scan fixture (Node), 11 September 2026
// Companion to the Python fixture. Deliberately different defect classes:
// path traversal, XSS, SSRF, weak randomness, prototype pollution and ReDoS
// do not appear there, so the two together test more of the ruleset.

const express = require('express')
const fs = require('fs')
const path = require('path')
const crypto = require('crypto')
const { exec } = require('child_process')
const jwt = require('jsonwebtoken')

const app = express()
app.use(express.json())

const JWT_SECRET = 'fixture-signing-key-do-not-ship'      // 1. hardcoded secret

// 2. path traversal — user input joined onto a base directory unchecked
app.get('/file', (req, res) => {
  res.send(fs.readFileSync(path.join('/srv/uploads', req.query.name), 'utf8'))
})

// 3. reflected XSS — request data written into HTML unescaped
app.get('/hello', (req, res) => {
  res.send(`<h1>Hello ${req.query.name}</h1>`)
})

// 4. SSRF — server fetches a URL the caller ch
app.get('/preview', async (req, res) => {
  const r = await fetch(req.query.url)
  res.send(await r.text())
})

// 5. weak randomness for a security token
function resetToken() {
  return Math.random().toString(36).slice(2)
}

// 6. prototype pollution — recursive merge with no key guard
function merge(target, source) {
  for (const k in source) {
    if (typeof source[k] === 'object' && source
      target[k] = merge(target[k] || {}, source[k])
    } else {
      target[k] = source[k]
    }
  }
  return target
}
app.post('/settings', (req, res) => res.json(me

// 7. ReDoS — catastrophic backtracking on atta
app.get('/validate', (req, res) => {
  res.json({ ok: /^(a+)+$/.test(req.query.v ||
})

// 8. command injection
app.get('/logs', (req, res) => {
  exec(`tail -n 50 /var/log/${req.query.service}.log`, (e, out) => res.send(out))
})

// 9. JWT verified with algorithms unrestricted
app.get('/me', (req, res) => {
  res.json(jwt.verify(req.headers.authorization
})

// 10. secret written to logs
console.log('booting with secret', JWT_SECRET)

app.listen(3000)
