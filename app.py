
// Testing-repo — Sekura scan fixture (Go), 11 September 2026
// Third companion to the Python and JavaScript fixtures. Go-specific shapes:
// math/rand for secrets, InsecureSkipVerify, DES, and an ignored error on a
// security-relevant call — none of which the other two exercise.

package main

import (
      "crypto/des"
      "crypto/md5"
      "crypto/tls"
      "database/sql"
      "fmt"
      "math/rand"
      "net/http"
      "os/exec"
      "path/filepath"
      "os"
)

const dbPassword = "fixture-pg-9f3a1c7d" // 1. hardcoded credential

var db *sql.DB

// 2. SQL injection — request data formatted into the statement
func user(w http.ResponseWriter, r *http.Request) {
      q := fmt.Sprintf("SELECT email FROM users WHERE name = '%s'", r.URL.Query().Get("name"))
      rows, _ := db.Query(q) // 3. error ignored on a query that can fail open
      defer rows.Close()
      for rows.Next() {
              var e string
              rows.Scan(&e)
              fmt.Fprintln(w, e)
      }
}

// 4. command injection — shell metacharacters reach sh
func logs(w http.ResponseWriter, r *http.Request) {
      out, _ := exec.Command("sh", "-c", "tail -n 50 /var/log/"+r.URL.Query().Get("svc")+".log").Output()
      w.Write(out)
}

// 5. path traversal — Join cleans the path but does not confine it
func download(w http.ResponseWriter, r *http.Request) {
      b, err := os.ReadFile(filepath.Join("/srv/files", r.URL.Query().Get("f")))
      if err != nil {
              http.Error(w, "not found", 404)
              return
      }
      w.Write(b)
}

// 6. predictable token — math/rand, not crypto/rand
func resetToken() string {
      b := make([]byte, 16)
      for i := range b {
              b[i] = byte(rand.Intn(256))
      }
      return fmt.Sprintf("%x", b)
}

// 7. weak hash for a password
func hashPassword(p string) string {
      return fmt.Sprintf("%x", md5.Sum([]byte(p)))
}

// 8. broken cipher
func encrypt(key, data []byte) []byte {
      block, _ := des.NewCipher(key)
      out := make([]byte, 8)
      block.Encrypt(out, data[:8])
      return out
}

// 9. TLS verification disabled on an outbound client
func fetch(url string) (*http.Response, error) {
      c := &http.Client{Transport: &http.Transport{
              TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
      }}
      return c.Get(url)
}

func main() {
      http.HandleFunc("/user", user)
      http.HandleFunc("/logs", logs)
      http.HandleFunc("/download", download)
      // 10. no timeouts on a public listener
      http.ListenAndServe(":8080", nil)
}
