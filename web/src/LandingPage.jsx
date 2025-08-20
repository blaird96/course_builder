import './LandingPage.css'
import React, { useState } from 'react'

function LandingPage() {
  const [tree, setTree] = useState([])
  const [calendar, setCalendar] = useState([])

  const testApiPreview = async () => {
    const plan = {
      root: "/courses/Example",
      course_name: "Example Course",
      weeks: [
        { index: 1, title: "Week_1" },
        { index: 2, title: "Week_2" }
      ]
    }
    try {
      const res = await fetch('/plan/preview', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(plan)
      })
      if (!res.ok) {
        console.error('API error', res.status)
        return
      }
      const data = await res.json()
      setTree(data.tree || [])
      setCalendar(data.calendar || [])
    } catch (err) {
      console.error(err)
    }
  }

  return (
    <main className="landing">
      <section className="hero">
        <h1>Course Builder</h1>
        <p>Create, manage, and share interactive courses right from your browser.</p>
        <a href="#" className="cta" onClick={(e)=>{e.preventDefault(); testApiPreview();}}>Get Started</a>
      </section>

      <section className="test-section">
        <button onClick={testApiPreview}>Test API</button>
        {tree.length > 0 && (
          <div className="api-preview">
            <h3>Directory Tree</h3>
            <ul>
              {tree.map((t, idx) => <li key={idx}>{t}</li>)}
            </ul>
          </div>
        )}
        {calendar.length > 0 && (
          <div className="api-preview">
            <h3>Calendar</h3>
            <ul>
              {calendar.map((c, idx) => <li key={idx}>{c}</li>)}
            </ul>
          </div>
        )}
      </section>

      <section className="features">
        <div className="feature">
          <h2>Simple Authoring</h2>
          <p>Compose lessons using markdown and rich, interactive components.</p>
        </div>
        <div className="feature">
          <h2>Collaboration</h2>
          <p>Work together with your team and track progress in real time.</p>
        </div>
        <div className="feature">
          <h2>Extensible</h2>
          <p>Built on open standards so you can customize and extend.</p>
        </div>
      </section>
    </main>
  )
}

export default LandingPage
