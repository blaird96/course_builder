import './LandingPage.css'

function LandingPage() {
  return (
    <main className="landing">
      <section className="hero">
        <h1>Course Builder</h1>
        <p>Create, manage, and share interactive courses right from your browser.</p>
        <a href="#" className="cta">Get Started</a>
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

