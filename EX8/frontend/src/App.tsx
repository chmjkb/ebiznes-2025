import { useState, useEffect } from 'react'
import './App.css'

interface User {
  username: string
  token: string
}

function App() {
  const [user, setUser] = useState<User | null>(null)
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [isLoginMode, setIsLoginMode] = useState(true)

  useEffect(() => {
    // Listen for OAuth callback messages
    const handleMessage = (event: MessageEvent) => {
      if (event.origin !== 'http://localhost:8000') return
      
      if (event.data.type === 'oauth-callback') {
        setUser({
          username: event.data.username,
          token: event.data.token
        })
      }
    }

    window.addEventListener('message', handleMessage)
    return () => window.removeEventListener('message', handleMessage)
  }, [])

  const handleGoogleLogin = () => {
    const width = 500
    const height = 600
    const left = window.screenX + (window.outerWidth - width) / 2
    const top = window.screenY + (window.outerHeight - height) / 2
    
    window.open(
      'http://localhost:8000/auth/login/google',
      'Google OAuth',
      `width=${width},height=${height},left=${left},top=${top}`
    )
  }

  const handleGithubLogin = () => {
    const width = 500
    const height = 600
    const left = window.screenX + (window.outerWidth - width) / 2
    const top = window.screenY + (window.outerHeight - height) / 2
    
    window.open(
      'http://localhost:8000/auth/login/github',
      'GitHub OAuth',
      `width=${width},height=${height},left=${left},top=${top}`
    )
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')

    const endpoint = isLoginMode ? 'login' : 'register'

    try {
      const response = await fetch(`http://localhost:8000/auth/${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Request failed')
      }

      const data = await response.json()
      setUser(data)
      setUsername('')
      setPassword('')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Request failed')
    }
  }

  const handleLogout = async () => {
    if (!user) return

    try {
      await fetch('http://localhost:8000/auth/logout', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${user.token}`,
        },
      })
      setUser(null)
    } catch (err) {
      console.error('Logout failed:', err)
    }
  }

  if (user) {
    return (
      <div className="container">
        <h1>Welcome, {user.username}!</h1>
        <p>You are successfully logged in.</p>
        <button onClick={handleLogout}>Logout</button>
      </div>
    )
  }

  return (
    <div className="container">
      <h1>{isLoginMode ? 'Login' : 'Register'}</h1>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="username">Username</label>
          <input
            type="text"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            minLength={isLoginMode ? 1 : 3}
          />
        </div>
        <div className="form-group">
          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            minLength={isLoginMode ? 1 : 6}
          />
        </div>
        {error && <div className="error">{error}</div>}
        <button type="submit">{isLoginMode ? 'Login' : 'Register'}</button>
      </form>
      {isLoginMode && (
        <>
          <div className="divider">
            <span>OR</span>
          </div>
          <button onClick={handleGoogleLogin} className="google-button">
            Sign in with Google
          </button>
          <button onClick={handleGithubLogin} className="github-button">
            Sign in with GitHub
          </button>
        </>
      )}
      <div className="toggle-mode">
        <p>
          {isLoginMode ? "Don't have an account? " : "Already have an account? "}
          <a href="#" onClick={(e) => {
            e.preventDefault()
            setIsLoginMode(!isLoginMode)
            setError('')
          }}>
            {isLoginMode ? 'Register' : 'Login'}
          </a>
        </p>
      </div>
      {isLoginMode && (
        <div className="hint">
          <p>Test users: admin/admin123 or user/user123</p>
        </div>
      )}
    </div>
  )
}

export default App
